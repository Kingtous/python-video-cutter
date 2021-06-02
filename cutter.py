import sys
import optparse

from video_processer import VideoProcesser

def init_parser() -> optparse.OptionParser:
    parser = optparse.OptionParser()
    parser.add_option('-i','--input',dest='file',help='输入文件')
    parser.add_option('-o','--output',dest='output',help='输出文件')
    parser.add_option('-s','--start',dest='start',help='开始时间：实例"00:00:00"')
    parser.add_option('-e','--end',dest='end',help='结束时间：实例"00:00:59"')
    return parser

if __name__ == '__main__':
    # global variable
    parser = init_parser()
    opts,args = parser.parse_args(sys.argv[1:])
    input_file = opts.file
    output_file = opts.output
    st_time = opts.start
    ed_time = opts.end
    if input is None or output_file is None:
        print('未指定输入输出，请使用-h或者--help查看帮助')
        exit(0)
    video_processer = VideoProcesser(input_file,output_file)
    if (video_processer.cut(st_time,ed_time)):
        video_processer.beginProcess()
    else:
        print('时间未按格式输入，格式：00:00:00')