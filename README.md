# fg_voice_assistant
 Voice assistant for FlightGear

1. Install libraries from requirements.txt
2. Download VOSK model for you language and paste it in voice_interface.py
3. move t154.xml to FG_ROOT/Protocol
4. run FG with --generic=socket,out,5,127.0.0.1,5701,udp,t154
5. run voice_interface.py and main.py