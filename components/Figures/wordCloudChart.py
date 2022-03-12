import numpy as np
from wordcloud import WordCloud
from io import BytesIO
import base64
import random

def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)


def wordCloudChart(df):
    # делаем масску в виде круга
    x, y = np.ogrid[:300, :300]
    mask = (x - 150) ** 2 + (y - 150) ** 2 > 130 ** 2
    mask = 255 * mask.astype(int)

    df_wc = df.groupby(['epithets'])[['epithets']].count()
    unique_words = df_wc.index.tolist()
    freqs = df_wc['epithets'].tolist()
    d = {w: f for w, f in zip(unique_words, freqs)}

    img = BytesIO()
    wc = WordCloud(background_color='white',
                   color_func=lambda *args, **kwargs: "black",
                   width=500, height=500, min_font_size=10,
                   max_font_size=70, random_state=5,
                   prefer_horizontal=1,
                   mask=mask).fit_words(d)

    # переводим изображение в формат base64
    wc.to_image().save(img, format='PNG')
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())

