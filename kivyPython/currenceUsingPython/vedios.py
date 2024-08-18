from kivy.app import App
from kivy.uix.video import Video

class VideoPlayerApp(App):
    def build(self):
        # تحديد ملف الفيديو
        video_source = 'path/to/your/video.mp4'

        # إنشاء عنصر الفيديو
        video = Video(source=video_source, state='play', options={'allow_stretch': True})

        # إعداد حجم النافذة
        self.root = video
        return self.root

if __name__ == '__main__':
    VideoPlayerApp().run()
