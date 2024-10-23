import React, { useState, useEffect, useRef } from 'react';
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import { AlertCircle } from "lucide-react"

interface LogEntry {
  timestamp: string;
  message: string;
  type: 'info' | 'error';
}

export default function Component() {
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [errorKeyword, setErrorKeyword] = useState('ERROR');
  const [isMonitoring, setIsMonitoring] = useState(false);
  const scrollAreaRef = useRef<HTMLDivElement>(null);
  const audioRef = useRef<HTMLAudioElement>(null);

  useEffect(() => {
    let intervalId: NodeJS.Timeout;

    const fetchLogs = async () => {
      // Simulating log fetching. In a real implementation, this would connect to your backend.
      const newLog: LogEntry = {
        timestamp: new Date().toISOString(),
        message: `Log entry at ${new Date().toLocaleTimeString()}`,
        type: Math.random() > 0.9 ? 'error' : 'info', // 10% chance of error for demonstration
      };

      setLogs(prevLogs => [...prevLogs.slice(-99), newLog]);

      if (newLog.type === 'error' && newLog.message.toUpperCase().includes(errorKeyword.toUpperCase())) {
        handleError(newLog);
      }
    };

    if (isMonitoring) {
      intervalId = setInterval(fetchLogs, 1000);
    }

    return () => {
      if (intervalId) clearInterval(intervalId);
    };
  }, [isMonitoring, errorKeyword]);

  useEffect(() => {
    if (scrollAreaRef.current) {
      scrollAreaRef.current.scrollTop = scrollAreaRef.current.scrollHeight;
    }
  }, [logs]);

  const handleError = (errorLog: LogEntry) => {
    if (audioRef.current) {
      audioRef.current.play();
    }
    console.error('Error detected:', errorLog.message);
    // Simulating queueing next image. In a real implementation, this would interact with ComfyUI.
    console.log('Queueing next image...');
  };

  const toggleMonitoring = () => {
    setIsMonitoring(prev => !prev);
  };

  return (
    <div className="w-full max-w-4xl mx-auto p-6 space-y-4">
      <h2 className="text-2xl font-bold">Interactive Log Monitor</h2>
      <div className="flex space-x-2">
        <Input
          type="text"
          placeholder="Error keyword"
          value={errorKeyword}
          onChange={(e) => setErrorKeyword(e.target.value)}
          className="flex-grow"
        />
        <Button onClick={toggleMonitoring} variant={isMonitoring ? "destructive" : "default"}>
          {isMonitoring ? 'Stop Monitoring' : 'Start Monitoring'}
        </Button>
      </div>
      <ScrollArea className="h-[400px] border rounded-md p-4 bg-black" ref={scrollAreaRef}>
        {logs.map((log, index) => (
          <div key={index} className={`mb-1 ${log.type === 'error' ? 'text-red-500' : 'text-green-500'}`}>
            <span className="text-gray-400">[{log.timestamp}] </span>
            {log.message}
            {log.type === 'error' && <AlertCircle className="inline ml-2" size={16} />}
          </div>
        ))}
      </ScrollArea>
      <audio ref={audioRef} src="/custom_nodes/ComfyUI_BWiZ_Nodes/res/js/assets/error.mp3" />
    </div>
  );
}