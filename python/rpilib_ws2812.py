# piolib_ws2812.py
import time
from rpi_ws281x import PixelStrip as Adafruit_NeoPixel, Color

class LedType:
    GRB = 0
    RGB = 1
    BRG = 2
    RBG = 3
    GBR = 4
    BGR = 5

class WS2812:
    def __init__(self, led_count=8, led_pin=18, led_freq_hz=800000, led_dma=10, 
                 led_brightness=255, led_invert=False, led_channel=0, order="RGB"):
        """
        初始化WS2812控制器
        
        Args:
            led_count: LED数量
            led_pin: GPIO引脚号
            led_freq_hz: LED信号频率
            led_dma: DMA通道
            led_brightness: LED亮度(0-255)
            led_invert: 是否反转信号
            led_channel: 通道号
            order: LED颜色顺序
        """
        self.ORDER = order
        self.led_type_map = {
            "GRB": LedType.GRB,
            "RGB": LedType.RGB,
            "BRG": LedType.BRG,
            "RBG": LedType.RBG,
            "GBR": LedType.GBR,
            "BGR": LedType.BGR
        }
        
        # 创建LED对象
        self.strip = Adafruit_NeoPixel(
            led_count, led_pin, led_freq_hz, led_dma, 
            led_invert, led_brightness, led_channel
        )
        self.strip.begin()
        
    def get_led_type(self):
        """获取LED类型"""
        return self.led_type_map.get(self.ORDER, LedType.GRB)
        
    def set_brightness(self, brightness):
        """
        设置LED亮度
        
        Args:
            brightness: 亮度值(0-255)
        """
        self.strip.setBrightness(brightness)
        
    def get_brightness(self):
        """获取当前亮度设置"""
        # 注意：Adafruit库没有直接获取亮度的方法，这里返回最后设置的值
        pass  # 需要在类中保存亮度值才能实现此功能
        
    def set_pixel_color_data(self, index, color):
        self.strip.setPixelColor(index, color)

    def set_all_pixel_color(self, color):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, self._led_type_convert(r, g, b))
        self.strip.show()

    def set_pixel_rgb_data(self, index, r, g, b):
        color = self._led_type_convert(r, g, b)
        self.strip.setPixelColor(index, color)
        
    def set_all_pixel_rgb(self, r, g, b):
        for i in range(self.strip.numPixels()):
            color = self._led_type_convert(r, g, b)
            self.strip.setPixelColor(i, color)
        self.strip.show()   

    def _led_type_convert(self, r, g, b):
        led_types = ["GRB", "GBR", "RGB", "RBG", "BRG", "BGR"]
        colors = [
            Color(g, r, b), Color(g, b, r), Color(r, g, b), 
            Color(r, b, g), Color(b, r, g), Color(b, g, r)
        ]
        
        if self.ORDER in led_types:
            return colors[led_types.index(self.ORDER)]
        return Color(r, g, b)
        
    def show(self):
        """显示所有LED"""
        self.strip.show()
        
    def clear(self):
        """清除所有LED"""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color(0, 0, 0))
        self.strip.show()
        
    def num_pixels(self):
        """获取LED数量"""
        return self.strip.numPixels()
        
    def wheel(self, pos):
        """
        生成彩虹色
        
        Args:
            pos: 位置(0-255)
            
        Returns:
            Color对象
        """
        if pos < 0 or pos > 255:
            r = g = b = 0
        elif pos < 85:
            r = pos * 3
            g = 255 - pos * 3
            b = 0
        elif pos < 170:
            pos -= 85
            r = 255 - pos * 3
            g = 0
            b = pos * 3
        else:
            pos -= 170
            r = 0
            g = pos * 3
            b = 255 - pos * 3
        return self._led_type_convert(r, g, b)

if __name__ == "__main__":
    import sys
    strip = None  
    try:
        # 修改这一行：LedType.LED_TYPE_GRB -> LedType.GRB
        strip = WS2812(led_pin=18, led_count=8, order="RGB")
        print("WS2812 initialization successful")
        print("Press Ctrl+C to exit program")
        
        strip.set_brightness(100)
        
        strip.set_all_pixel_rgb(255, 0, 0) 
        strip.show()
        time.sleep(1)

        strip.set_all_pixel_rgb(0, 255, 0) 
        strip.show()
        time.sleep(1)

        strip.set_all_pixel_rgb(0, 0, 255) 
        strip.show()
        time.sleep(1)

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        if strip is not None:
            strip.clear()  # rpilib_ws2812使用clear()方法而不是deinit()
        sys.exit(1)