import re
import queue
import asyncio

try:
    from ffmpeg import FFmpeg
except:
    print('没有找到python-ffmpeg,自动安装中')
    from pip._internal import main
    main(['install','python-ffmpeg'])
    from ffmpeg import FFmpeg

class VideoTask:
    
    def execute(self):
        pass

class VideoCutTaskWrapper(VideoTask):
    
    def __init__(self,input_path:str,output_path:str,st_time:str,ed_time:str) -> None:
        self.input_path = input_path
        self.output_path = output_path
        self.st_time = st_time
        self.ed_time = ed_time
        
    def execute(self):
        ffmpeg =FFmpeg().option('y').input(self.input_path).output(self.output_path,{
            'ss':self.st_time,
            'to':self.ed_time
        })
        
        @ffmpeg.on('start')
        def ffmpeg_start(arguments):
            print('开始裁剪视频：',self.input_path)
            print('输出至：',self.output_path)
            print('裁剪时间段：',self.st_time,'-',self.ed_time)
        
        @ffmpeg.on('error')
        def ffmpeg_err(err):
            print('裁剪出现错误，错误号：',err)
        
        @ffmpeg.on('progress')
        def ffmpeg_progress(progress):
            print('处理进度',progress)
        
        @ffmpeg.on('completed')
        def ffmpeg_complete():
            print('裁剪完成',self.output_path)
            pass
        
        loop = asyncio.get_event_loop()
        loop.run_until_complete(ffmpeg.execute())
        loop.close()

class VideoProcesser:
    
    def __init__(self,path:str,output:str) -> None:
        self.path = path
        self.output = output
        self.timeformat = re.compile(r'\d\d:\d\d:\d\d')
        self.q = queue.Queue()
    
    # 格式
    # st_time: 00:00:00
    # ed_time: 00:00:00
    def cut(self,st_time:str,ed_time:str) -> bool:
        if not self.timeformat.match(st_time) or not self.timeformat.match(ed_time):
            return False
        else:
            self.q.put(VideoCutTaskWrapper(self.path,self.output,st_time,ed_time))
            return True
            
            
    def beginProcess(self):
        while not self.q.empty():
            task = self.q.get()
            if task.__class__.__base__ == VideoTask:
                task.execute()
            
    
    
