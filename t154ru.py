from text_to_num import text2num


class Addon():
    text = ''
    props2post = list()
    SPEEDS_BORDERS = [140, 160, 180, 200, 220, 221, 222, 223]
    SPEEDS_WORDS = ['140', '160', '180', '200','220', 'рубеж', 'подъем', 'безопасная']
    INPUT_PROTOCOL = '!iiii'#int int int int
    '''
    fdm/jsbsim/instrumentation/vc-kmh
    fdm/jsbsim/instrumentation/v-1
    fdm/jsbsim/instrumentation/v-r
    fdm/jsbsim/instrumentation/v-2
    '''
    OUTPUT_PROTOCOL = ''

    def __init__(self):
        pass

    def update_speed(self):
        self.SPEEDS_BORDERS[5] = self.properties[1]
        self.SPEEDS_BORDERS[6] = self.properties[2]
        self.SPEEDS_BORDERS[7] = self.properties[3]


    speed_flag = -1
    def voice_speed(self):
        #---
        speed = self.properties[0]

        new_speed_flag = sorted(self.SPEEDS_BORDERS + [speed]).index(speed) - 1
        if self.speed_flag != new_speed_flag:
            self.speed_flag = new_speed_flag
            if self.speed_flag == 2:
                self.update_speed()
            return self.SPEEDS_WORDS[self.speed_flag]
        return ''

    def update(self, data) -> tuple[list, str]:
        # returns list of variables for simulator and text for speaking
        if data is None:
            return [], ''
        self.properties = data
        self.text += self.voice_speed()
        return [], self.voice_speed()
    
    def gear_up(self):
        self.text += 'шасси убираются'
        self.props2post.append({'name':'/controls/gear/gear-down', 'value':0})
        self.props2post.append({'name':'/tu154/gear/sw-main', 'value':-1})
    
    def gear_neutr(self):
        self.text += 'кран шасси нейтрально установлен'
        self.props2post.append({'name':'/tu154/gear/sw-main', 'value':0})    
    
    def gear_down(self):
        self.text += 'шасси выпускаются'
        self.props2post.append({'name':'/controls/gear/gear-down', 'value':1})
        self.props2post.append({'name':'/tu154/gear/sw-main', 'value':1})

    def set_engines(self, throttle):
        for i in range(3):
            self.props2post.append({'name':f'/controls/engines/engine[{i}]/throttle', 'value':throttle})

    def update_voice(self, text):
        if 'шасси' in text or 'шоссе' in text:
            if 'брать' in text:
                self.gear_up()
            elif 'кран' in text or 'нейтральн' in text:
                self.gear_neutr()
            elif 'выпустить' in text:
                self.gear_down()
        elif 'режим' in text or text == 'малый газ':
            if 'взлёт' in text:
                self.text += 'режим взлётный, руд держу'
                throttle = 1
            elif 'малый' in text:
                self.text += 'малый газ'
                throttle = 0
            elif 'номинал' in text:
                self.text += 'номинальный режим'
                throttle = 0.93
            else:
                throttle = (text2num(text[6:], 'ru') - 53) / 45
            self.set_engines(throttle)
        elif text.startswith('закрылки'):
            self.text += text
            if text == 'закрылки убрать' or text == 'закрылки ноль':
                self.props2post.append({'name':'/controls/flight/flaps', 'value':0})
            elif text == 'закрылки пятнадцать':
                self.props2post.append({'name':'/controls/flight/flaps', 'value':0.3333})
            elif text == 'закрылки двадцать восемь':
                self.props2post.append({'name':'/controls/flight/flaps', 'value':0.62})
            elif text == 'закрылки сорок пять':
                self.props2post.append({'name':'/controls/flight/flaps', 'value':1})
        elif 'реверс' in text:
            self.props2post.append({'name':'/fdm/jsbsim/fcs/revers-by-key', 'value':1})
        elif 'уход' in text:
            self.gear_up()
            self.set_engines(1)
            
    def get_text(self):
        text = self.text
        self.text = ''
        return text
    
    def get_props2post(self) -> list:
        vars = self.props2post.copy()
        self.props2post = []
        return vars