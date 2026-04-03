import React, { useState, useRef, useEffect } from 'react';
import PropTypes from 'prop-types';

const MicIcon = ({ isRecording }) => (
    <svg viewBox="0 0 24 24" width="32" height="32" stroke={isRecording ? "#ff4d4d" : "#555"} strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round" style={{ transition: 'stroke 0.3s' }}>
        <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
        <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
        <line x1="12" y1="19" x2="12" y2="23"></line>
        <line x1="8" y1="23" x2="16" y2="23"></line>
    </svg>
);

const DashAudioRecorder = (props) => {
    // 1. ADDED: streamMode (setting), audioStream (output), currentVolume (output)
    const { id, setProps, audioType, visualMode, recordMode, echoCancellation, noiseSuppression, autoGainControl, streamMode } = props;
    const [isRecording, setIsRecording] = useState(false);
    
    const canvasRef = useRef(null);
    const mediaRecorderRef = useRef(null);
    const audioContextRef = useRef(null);
    const animationRef = useRef(null);
    const volumeIntervalRef = useRef(null); // NEW: Interval for volume meter
    const chunksRef = useRef([]);
    const isPressingRef = useRef(false);

    useEffect(() => {
        const handleGlobalUp = () => {
            if (recordMode === 'hold') {
                isPressingRef.current = false;
                stopRecording();
            }
        };
        window.addEventListener('mouseup', handleGlobalUp);
        window.addEventListener('touchend', handleGlobalUp);
        return () => {
            window.removeEventListener('mouseup', handleGlobalUp);
            window.removeEventListener('touchend', handleGlobalUp);
        };
    });

    const startRecording = async () => {
        if (isRecording) return;
        if (recordMode === 'hold') isPressingRef.current = true;
        
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ 
                audio: {
                    echoCancellation: echoCancellation,
                    noiseSuppression: noiseSuppression,
                    autoGainControl: autoGainControl
                } 
            });
            
            if (recordMode === 'hold' && !isPressingRef.current) {
                stream.getTracks().forEach(track => track.stop());
                return;
            }

            audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)();
            const source = audioContextRef.current.createMediaStreamSource(stream);
            const analyser = audioContextRef.current.createAnalyser();
            analyser.fftSize = 2048;
            source.connect(analyser);

            let mimeType = audioType;
            if (!MediaRecorder.isTypeSupported(mimeType)) mimeType = ''; 

            const recorderOptions = mimeType ? { mimeType } : {};
            recorderOptions.audioBitsPerSecond = 128000; 

            mediaRecorderRef.current = new MediaRecorder(stream, recorderOptions);
            chunksRef.current = [];

            // 2. LOGIC SEPARATION: Stream vs. Normal Mode
            mediaRecorderRef.current.ondataavailable = (e) => {
                if (e.data.size > 0) {
                    if (streamMode) {
                        // STREAM MODE: Send chunk immediately to Python via audioStream
                        const reader = new FileReader();
                        reader.readAsDataURL(e.data);
                        reader.onloadend = () => {
                            if (setProps) setProps({ audioStream: reader.result });
                        };
                    } else {
                        // NORMAL MODE: Collect chunks in memory
                        chunksRef.current.push(e.data);
                    }
                }
            };

            // 3. FINALIZATION: Only send complete data if not in stream mode
            mediaRecorderRef.current.onstop = () => {
                if (!streamMode) {
                    const blob = new Blob(chunksRef.current, { type: mimeType || 'audio/webm' });
                    const reader = new FileReader();
                    reader.readAsDataURL(blob);
                    reader.onloadend = () => {
                        if (setProps) setProps({ audioData: reader.result });
                    };
                }
            };

            // NEW: Measure volume and send it to Python (0-128 scale)
            volumeIntervalRef.current = setInterval(() => {
                if (!analyser) return;
                const bufferLength = analyser.frequencyBinCount;
                const dataArray = new Uint8Array(bufferLength);
                analyser.getByteTimeDomainData(dataArray);
                
                let maxVolume = 0;
                for (let i = 0; i < bufferLength; i++) {
                    let v = Math.abs(dataArray[i] - 128); // Calculate absolute difference from center line (128)
                    if (v > maxVolume) maxVolume = v;
                }
                
                if (setProps) setProps({ currentVolume: maxVolume });
            }, 100); // Trigger 10 times per second

            // 4. START: Handle chunk intervals if streaming
            if (streamMode) {
                // Request data every 150ms
                mediaRecorderRef.current.start(150); 
            } else {
                // Let it record until stopped
                mediaRecorderRef.current.start();
            }
            
            setIsRecording(true);
            drawWaveform(analyser);

        } catch (err) {
            console.error("Error accessing microphone:", err);
            alert("Please allow microphone access in your browser.");
        }
    };

    const stopRecording = () => {
        if (mediaRecorderRef.current && mediaRecorderRef.current.state !== "inactive") {
            mediaRecorderRef.current.stop();
            mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
            setIsRecording(false);
            if (audioContextRef.current) audioContextRef.current.close();
            if (animationRef.current) cancelAnimationFrame(animationRef.current);
            if (volumeIntervalRef.current) clearInterval(volumeIntervalRef.current); // NEW: Clear interval
        }
    };

    const drawWaveform = (analyser) => {
        const draw = () => {
            animationRef.current = requestAnimationFrame(draw);
            const canvas = canvasRef.current;
            if (!canvas) return;

            const isFull = visualMode === 'fullscreen';
            
            if (isFull) {
                if (canvas.width !== window.innerWidth) canvas.width = window.innerWidth;
                if (canvas.height !== window.innerHeight) canvas.height = window.innerHeight;
            } else {
                if (canvas.width !== 300) canvas.width = 300;
                if (canvas.height !== 100) canvas.height = 100;
            }

            const canvasCtx = canvas.getContext("2d");
            const bufferLength = analyser.frequencyBinCount;
            const dataArray = new Uint8Array(bufferLength);
            
            analyser.getByteTimeDomainData(dataArray);

            const width = canvas.width;
            const height = canvas.height;

            canvasCtx.fillStyle = isFull ? 'rgba(15, 15, 20, 0.95)' : 'rgb(240, 240, 240)';
            canvasCtx.fillRect(0, 0, width, height);
            canvasCtx.lineWidth = isFull ? 4 : 2;
            canvasCtx.strokeStyle = isRecording ? '#ff4d4d' : 'rgb(30, 144, 255)';
            canvasCtx.beginPath();

            const sliceWidth = width * 1.0 / bufferLength;
            let x = 0;
            const amplitudeMultiplier = isFull ? 3.0 : 1.0;

            for (let i = 0; i < bufferLength; i++) {
                let v = dataArray[i] / 128.0; 
                v = ((v - 1.0) * amplitudeMultiplier) + 1.0; 
                const y = v * height / 2;
                if (i === 0) canvasCtx.moveTo(x, y);
                else canvasCtx.lineTo(x, y);
                x += sliceWidth;
            }
            canvasCtx.lineTo(width, height / 2);
            canvasCtx.stroke();
        };
        draw();
    };

    const isFull = visualMode === 'fullscreen';
    const containerStyle = isFull && isRecording ? {
        position: 'fixed', top: 0, left: 0, width: '100vw', height: '100vh', zIndex: 99999, 
        display: 'flex', justifyContent: 'center', alignItems: 'center', backgroundColor: 'rgba(15, 15, 20, 0.95)'
    } : {
        display: 'inline-block', textAlign: 'center', fontFamily: 'sans-serif'
    };

    const canvasStyle = isFull && isRecording ? {
        position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', zIndex: -1
    } : {
        backgroundColor: '#f0f0f0', borderRadius: '8px', marginTop: '15px', 
        display: isFull ? 'none' : 'block'
    };

    const buttonStyle = {
        backgroundColor: isRecording && isFull ? 'rgba(255, 255, 255, 0.1)' : 'white',
        border: isRecording && isFull ? '2px solid #ff4d4d' : '1px solid #ccc',
        padding: '20px', borderRadius: '50%', cursor: 'pointer',
        display: 'flex', justifyContent: 'center', alignItems: 'center',
        boxShadow: '0 4px 10px rgba(0,0,0,0.1)', transition: 'all 0.3s ease', zIndex: 1,
        userSelect: 'none', WebkitUserSelect: 'none' 
    };

    const handleStart = (e) => { e.preventDefault(); startRecording(); };
    const handleStop = (e) => { e.preventDefault(); stopRecording(); };

    let buttonEvents = {};
    if (recordMode === 'hold') {
        buttonEvents = { onMouseDown: handleStart, onTouchStart: handleStart };
    } else {
        buttonEvents = { onClick: isRecording ? handleStop : handleStart };
    }

    return (
        <div id={id} style={containerStyle}>
            <button 
                {...buttonEvents}
                style={buttonStyle}
                title={recordMode === 'hold' ? "Hold to record" : "Click to record"}>
                <MicIcon isRecording={isRecording} />
            </button>
            {(isRecording || !isFull) && (
                <canvas ref={canvasRef} style={canvasStyle}></canvas>
            )}
        </div>
    );
}

// 5. Default properties (backward compatibility maintained)
DashAudioRecorder.defaultProps = {
    audioData: null,
    audioStream: null,     
    currentVolume: 0,      // NEW
    audioType: 'audio/webm',
    visualMode: 'fullscreen',
    recordMode: 'hold',
    echoCancellation: false,
    noiseSuppression: false,
    autoGainControl: false,
    streamMode: false      // NEW (defaults to normal recording)
};

// 6. Property types
DashAudioRecorder.propTypes = {
    id: PropTypes.string,
    audioData: PropTypes.string,
    audioStream: PropTypes.string, 
    currentVolume: PropTypes.number, // NEW
    audioType: PropTypes.string,
    visualMode: PropTypes.string,
    recordMode: PropTypes.string,
    echoCancellation: PropTypes.bool,
    noiseSuppression: PropTypes.bool,
    autoGainControl: PropTypes.bool,
    streamMode: PropTypes.bool,    
    setProps: PropTypes.func
};

export default DashAudioRecorder;