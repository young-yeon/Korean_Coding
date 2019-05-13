class Trans:

    def __init__(self, file_name):
        self.func = {}
        self.data = {}
        self.if_set = []

        self.file_name = file_name
        self.file_data = "다." + self.file_open()
        self.check_if()
        self.check_func()
        self.to_do = self.spliting(self.file_data)
        self.to_do = self.to_do[1:len(self.to_do) - 1]

        for key in self.func.keys():
            tmp = self.spliting(self.func[key])
            self.func[key] = tmp[:len(tmp) - 1]


    def file_open(self):
        f = open(self.file_name, "r", encoding = "UTF-8")
        data = f.read()
        f.close()
        return data


    def run(self):
        for sentence in self.to_do:
            self.decode(sentence)
            
    
    def decode(self, sentence):
        if not len(sentence):
            return None
        if sentence[-1] == "이":
            self.substitude(sentence)
        elif sentence[-1] == "한":
            if sentence.find("반복") != -1:
                self.loop(sentence)
            else:
                self.calc(sentence)
        elif sentence[-1] == "같" or sentence[-1] == "르" or \
                sentence[-1] == "크" or sentence[-1] == "작":
            self.comp(sentence)
        elif sentence[-1] == "든":
            self.declare(sentence)
        elif sentence[-1] == "뺀" or sentence[-1] == "눈":
            self.calc(sentence)
        elif sentence[-1] == "하":
            self.printing(sentence)
        elif "if" in sentence:
            self.do_if(sentence)


    def check_if(self):
        while "라면 한다." in self.file_data:
            first_if = self.file_data.split("라면 한다.")
            idx = self.file_data.find("라면 한다.")
            if_name = first_if[0].split("만약")[-1]
            first_if = first_if[1]

            start_idx = self.file_data.find("만약")

            if not "이렇게" in self.file_data:
                print("조건문이 종결지어지지 않았습니다. code:1.5")
                exit(0)
            
            last_idx = self.file_data.find("이렇게.")
            condition = if_name.strip()
            self.if_set.append((condition[:len(condition)-1], first_if[:first_if.find("이렇게.")]))
            self.file_data = self.file_data[:start_idx] + \
                ("다. if : !%d! 다." % (len(self.if_set) - 1)) + \
                    self.file_data[last_idx + 4:]
    
    def check_func(self):
        while "하면 아래와 같이 한다." in self.file_data:
            first_func = self.file_data.split("하면 아래와 같이 한다.")
            idx = self.file_data.find("하면 아래와 같이 한다.")
            func_name = first_func[0].split("다.")[-1]
            first_func = first_func[1]

            start_idx = idx - len(func_name)

            if not "여기까지" in self.file_data:
                print("함수가 종결지어지지 않았습니다. code:1")
                exit(0)
            
            last_idx = self.file_data.find("여기까지.")
            self.func[func_name.strip()] = first_func[:first_func.find("여기까지.")]
            self.file_data = self.file_data[:start_idx] + self.file_data[last_idx + 5:]


    def spliting(self, file_data):
        data = file_data.split("다.")
        for i in range(len(data)):
            data[i] = data[i].strip()
        return data


    def declare(self, sentence):
        point = sentence.find("를 만든")
        if point == -1:
            point = sentence.find("을 만든")
            if point == -1:
                print("선언할 변수명을 입력해 주세요. code:2")
                exit(0)
        self.data[sentence[:point].strip()] = 0


    def substitude(self, sentence):
        n_point = sentence.find("는")
        if n_point == -1:
            n_point = sentence.find("은")
            if n_point == -1:
                print("문장에 대입할 대상이 없습니다. code:3")
                exit(0)
        v_point = sentence.find("이")
        name = sentence[:n_point].strip()
        try:
            if self.data[name]:
                check = True
        except KeyError:
            print("변수는 선언 후 사용해 주세요 code:4")
            exit(0)
        value = self.convert(sentence[n_point+1:v_point].strip())
        try:
            if self.data[value] or True:
                value = self.data[value]
        except:
            pass
        self.data[name] = value


    def convert(self, value):
        try:
            if int(value) == float(value):
                return int(value)
            else:
                return float(value)
        except:
            return value


    def loop(self, sentence):
        point = sentence.find("를")
        if point == -1:
            point = sentence.find("을")
            if point == -1:
                print("반복문에 함수명이 없습니다. code:5")
                exit(0)
        cnt_p = sentence.find("번 반복")
        if cnt_p == -1:
            print("반복 횟수가 없습니다. code:6")
            exit(0)
        cnt = self.convert(sentence[point+1:cnt_p].strip())
        if str(type(cnt)) != "<class 'int'>":
            print("반복 횟수는 숫자로 써주세요. code:7")
            exit(0)
        func_name = sentence[:point]
        to_do_list = self.func[func_name]
        for i in range(cnt):
            for do in to_do_list:
                self.decode(do)
    
    
    def do_if(self, sentence):
        num = int(sentence.split("!")[1])
        condition, to_do_list = self.if_set[num]
        flag = self.comp(condition)
        if flag:
            for do in to_do_list.split("다."):
                self.decode(do)


    def calc(self, sentence):
        n_point = sentence.find("에")
        if n_point == -1:
            print("계산할 대상이 없습니다. code:8")
            exit(0)
        v_point = sentence.find("을")
        if v_point == -1:
            v_point = sentence.find("를")
            if n_point == -1:
                print("계산할 크기가 없습니다. code:9")
                exit(0)
        name = sentence[:n_point].strip()
        value = self.convert(sentence[n_point+1:v_point].strip())
        if str(type(value)) != "<class 'int'>" and str(type(value)) != "<class 'float'>":
            try:
                if self.data[value]:
                    value = self.data[value]
            except: 
                print("연산 크기는 숫자로 써주세요. code:10")
                exit(0)
        try:
            if self.data[name]:
                check = True
        except KeyError:
            print("변수는 선언 후 사용해 주세요 code:11")
            exit(0)

        if "더한" in sentence:
            self.data[name] = self.data[name] + value
        elif "뺀" in sentence:
            self.data[name] = self.data[name] - value
        elif "곱한" in sentence:
            self.data[name] = self.data[name] * value
        elif "나눈" in sentence:
            self.data[name] = self.data[name] / value


    def comp(self, sentence):
        if "보다" in sentence:
            words, state = sentence.split("보다")
            point = words.find("가")
            if point == -1:
                point = words.find("이")
                if point == -1:
                    print("비교구문 해석 오류 code:12")
                    exit(0)
            a = words[:point]
            b = words[point+1:]
            a,b = a.strip(), b.strip()
            try:
                if self.data[a] and self.data[b]:
                    check = True
            except KeyError:
                print("변수는 선언 후 사용해 주세요 code:13")
                exit(0)
            if state[-1] == "크":
                return self.data[a] > self.data[b]
            elif state[-1] == "작":
                return self.data[a] < self.data[b]


        elif "와" in sentence:
            a,b_gb = sentence.split("와")
            if "가 다르" in b_gb:
                b = b_gb[:b_gb.find("가 다르")]
                a,b = a.strip(), b.strip()
                try:
                    if self.data[a] and self.data[b]:
                        check = True
                except KeyError:
                    print("변수는 선언 후 사용해 주세요 code:14")
                    exit(0)
                return self.data[a] != self.data[b]
            
            elif "가 같" in b_gb:
                b = b_gb[:b_gb.find("가 같")]
                a,b = a.strip(), b.strip()
                try:
                    if self.data[a] and self.data[b]:
                        check = True
                except KeyError:
                    print("변수는 선언 후 사용해 주세요 code:15")
                    exit(0)
                return self.data[a] == self.data[b]
            
            else:
                print("비교 구문 해석 오류 code:16")
                exit(0)
        else:
            print("비교불가 code:17")
            exit(0)
    

    def printing(self, sentence):
        if "계속" in sentence:
            point = sentence.find("계속")
            sentence = sentence[:point] + sentence[point + 2:]
            state = " "
        else:
            state = "\n"
    
        if "다 출력하" in sentence:
            sentence = sentence.split("다 출력하")[0]
            if sentence[-1] == "같" or sentence[-1] == "르" or \
                    sentence[-1] == "크" or sentence[-1] == "작":
                text = self.comp(sentence)
        else:
            point = sentence.find("출력하")
            key = sentence[:point].strip()
            try:
                text = self.data[key]
            except KeyError:
                text = key
        print(text, end = state)
