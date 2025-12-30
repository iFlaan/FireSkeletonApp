from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Ellipse
from kivy.clock import Clock
from kivy.core.window import Window
import math
import random

# إعدادات الشاشة للجوال
Window.clearcolor = (0.05, 0.02, 0, 1)

class SkeletonWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.num_segments = 25
        self.seg_len = 45 # المسافة بين المفاصل
        self.segments = []
        self.touch_pos = (Window.width/2, Window.height/2)
        self.is_touching = False
        self.time = 0
        self.current_speed = 0

        # إنشاء المفاصل
        for i in range(self.num_segments):
            self.segments.append({'x': Window.width/2, 'y': Window.height/2, 'angle': 0, 'w': 20})

        Clock.schedule_interval(self.update, 1.0/60.0)

    def on_touch_down(self, touch):
        self.is_touching = True
        self.touch_pos = touch.pos

    def on_touch_move(self, touch):
        self.touch_pos = touch.pos

    def on_touch_up(self, touch):
        self.is_touching = False

    def update(self, dt):
        self.time += 0.2
        head = self.segments[0]
        
        # منطق الحركة
        if self.is_touching:
            dx = self.touch_pos[0] - head['x']
            dy = self.touch_pos[1] - head['y']
            dist = math.hypot(dx, dy)
            target_speed = min(dist * 0.1, 15)
        else:
            target_speed = 0

        self.current_speed += (target_speed - self.current_speed) * 0.1

        if self.current_speed > 0.1:
            if self.is_touching:
                target_angle = math.atan2(dy, dx)
                diff = (target_angle - head['angle'] + math.pi) % (2 * math.pi) - math.pi
                head['angle'] += diff * 0.2
            
            head['x'] += math.cos(head['angle']) * self.current_speed
            head['y'] += math.sin(head['angle']) * self.current_speed

        # تحديث العمود الفقري
        for i in range(1, self.num_segments):
            prev = self.segments[i-1]
            curr = self.segments[i]
            dx_b = prev['x'] - curr['x']
            dy_b = prev['y'] - curr['y']
            angle = math.atan2(dy_b, dx_b)
            
            wave = math.sin(self.time - i * 0.5) * (2.0 / (self.current_speed + 1))
            curr['x'] = prev['x'] - math.cos(angle + wave) * self.seg_len
            curr['y'] = prev['y'] - math.sin(angle + wave) * self.seg_len
            curr['angle'] = angle

        self.draw_skeleton()

    def draw_skeleton(self):
        self.canvas.clear()
        with self.canvas:
            for i in range(self.num_segments - 1, -1, -1):
                seg = self.segments[i]
                ratio = i / self.num_segments
                
                # لون النار (أصفر إلى أحمر)
                Color(1, 1 - ratio, 0, 1)
                
                # رسم الأضلاع
                side_ang = seg['angle'] + math.pi/2
                w = 40 * (1 - ratio) if i > 5 else 15 + (i * 4)
                
                x1 = seg['x'] + math.cos(side_ang) * w
                y1 = seg['y'] + math.sin(side_ang) * w
                x2 = seg['x'] - math.cos(side_ang) * w
                y2 = seg['y'] - math.sin(side_ang) * w
                
                Line(points=[x1, y1, x2, y2], width=2)
                
                # رسم الرأس
                if i == 0:
                    Color(1, 1, 0.8, 1)
                    Ellipse(pos=(seg['x']-20, seg['y']-20), size=(40, 40))
                    # العيون
                    Color(0, 0, 0, 1)
                    Ellipse(pos=(seg['x']+5, seg['y']+5), size=(10, 10))
                    Ellipse(pos=(seg['x']-15, seg['y']+5), size=(10, 10))

class SkeletonApp(App):
    def build(self):
        return SkeletonWidget()

if __name__ == '__main__':
    SkeletonApp().run()
