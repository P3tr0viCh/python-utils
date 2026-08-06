import sys
from os import getcwd
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont

DEBUG = False

WEEKDAYS_RU = {
    0: 'понедельник',
    1: 'вторник',
    2: 'среда',
    3: 'четверг',
    4: 'пятница',
    5: 'суббота',
    6: 'воскресенье'
}

WIDTH, HEIGHT = 800, 600

COLOR_BACK = 'black'

COLOR_DATE = 'white'

SIZE_DATE = 48

FONT_DATE = ImageFont.truetype("arial.ttf", size=SIZE_DATE)

def create_img(date: datetime):
    date_weekday = WEEKDAYS_RU[date.weekday()]
    
    date_str = date.strftime("%Y-%m-%d")

    img = Image.new('RGB', (WIDTH, HEIGHT), color=COLOR_BACK)

    draw = ImageDraw.Draw(img)

    if DEBUG:
        draw.line([(0, HEIGHT // 2), (WIDTH, HEIGHT // 2)], fill='green', width=2)
        draw.line([(WIDTH // 2, 0), (WIDTH // 2, HEIGHT)], fill='green', width=2)

    date_bbox = draw.textbbox((0, 0), date_str, font=FONT_DATE)
    date_width = date_bbox[2] - date_bbox[0]
    date_height = date_bbox[3] - date_bbox[1]

    MAGIC_NUM = 14

    padding = 12

    date_x = (WIDTH - date_width) // 2
    date_y = HEIGHT // 2  - date_height - MAGIC_NUM - padding

    draw.text((date_x, date_y), date_str, fill=COLOR_DATE, font=FONT_DATE)

    date_bbox = draw.textbbox((0, 0), date_weekday, font=FONT_DATE)
    date_width = date_bbox[2] - date_bbox[0]
    date_height = date_bbox[3] - date_bbox[1]

    date_x = (WIDTH - date_width) // 2
    date_y = HEIGHT // 2 - MAGIC_NUM + padding

    draw.text((date_x, date_y), date_weekday, fill=COLOR_DATE, font=FONT_DATE)

    img.save(date_str + ' 00-00-00.png', 'PNG')

def main():
    if len(sys.argv) == 1:
        print('enter start and end dates. format: YYYY-MM-DD')

        date_start = input("start date: ")
        date_end = input("end date: ")
    elif len(sys.argv) == 2:
        print('enter end date. format: YYYY-MM-DD')

        date_start = sys.argv[1]
        date_end = input("end date: ")
    else:
        date_start = sys.argv[1]
        date_end = sys.argv[2]

    try:
        date_start = datetime.strptime(date_start, "%Y-%m-%d")
        date_end = datetime.strptime(date_end, "%Y-%m-%d")
    except ValueError:
        print('date has wrong format. format: YYYY-MM-DD')
        sys.exit(1)
            
    date = date_start

    while date <= date_end:
        create_img(date)
        
        date += timedelta(days=1)

    current_dir = getcwd()
    
    print(f'images saved into {current_dir}')
    
if __name__ == "__main__":
    main()