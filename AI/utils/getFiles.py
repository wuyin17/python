import fnmatch
import os


class GetFiles:
    def __init__(self, modelpath='models', modeltype='engine', videopath='video', videotype='mp4'):
        self.modelpath = modelpath
        self.modeltype = modeltype
        self.videopath = videopath
        self.videotype = videotype

    def getModels(self):
        # 列出当前目录下所有的.txt文件
        txt_files = fnmatch.filter(os.listdir(self.modelpath), f'*.{self.modeltype}')

        # 打印结果
        print(f"找到的{self.modeltype}文件:")
        for file in txt_files:
            print(file)
        return txt_files

    def getVideos(self):
        # 列出当前目录下所有的.txt文件
        txt_files = fnmatch.filter(os.listdir(self.videopath), f'*.{self.videotype}')

        # 打印结果
        print(f"找到的{self.videotype}文件:")
        for file in txt_files:
            print(file)
        return txt_files