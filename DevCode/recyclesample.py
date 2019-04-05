from kivy.app import App
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView


Builder.load_string('''
<RV>:
    viewclass: 'Label'
    RecycleBoxLayout:
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
''')

class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = [{'text': str(x)} for x in [["Bob", 4, 5], ["Mary", 3, 1], ["Bert", 9, 6]]]


class TestApp(App):
    def build(self):
        return RV()

if __name__ == '__main__':
    TestApp().run()
