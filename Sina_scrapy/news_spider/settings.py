import getopt


class Settings:
    __ADRESS__ = "0.0.0.0"
    __PORT__ = 8888
    # url
    list_url = "http://finance.sina.com.cn/7x24/?tag={}"

    __adress__ = "loaclhost"
    __port__ = 8888
    __type = "mongodb"
    __adressdb__ = "127.0.0.1"
    __portdb__ = 27017

    def __init__(self):
        #server
        self.__ADRESS__ = "0.0.0.0"
        self.__PORT__ = 8888
        # url
        self.list_url = "http://finance.sina.com.cn/7x24/?tag={}"

        self.__adress__ = "localhost"
        self.__port__ = 8888
        self.__type = "mongodb"
        self.__adressdb__ = "127.0.0.1"
        self.__portdb__ = 27017


    #根据sys.argv判断当前运行的是master还是slave
    def getCurrentMachine(self,argv):
        currentmachine = "slave"
        opts, args = getopt.getopt(argv[1:], '-m-s', ['master', 'slave'])
        for opt_name, opt_value in opts:
            if opt_name in ('-m', '--master'):
                currentmachine = "master"
                continue
            if opt_name in ('-s', '--slave'):
                currentmachine = "slave"
                continue
        return currentmachine
    #
    # http: // finance.sina.com.cn / 7x24 /?tag = {}
    def getName(self,object_scale):
        lastNum=object_scale[-1]

        if lastNum == '1':
            return "宏观"
        elif lastNum == '2':
            return "行业"
        elif lastNum == '3':
            return "公司"
        elif lastNum == '4':
            return "数据"
        elif lastNum == '5':
            return "市场"
        elif lastNum == '6':
            return "观点"
        elif lastNum == '7':
            return "央行"
        elif lastNum == '8':
            return "其他"
        elif lastNum == '9':
            return "A股"
        else:
            return " "
