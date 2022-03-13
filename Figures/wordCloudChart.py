import numpy as np
from wordcloud import WordCloud
from io import BytesIO
import base64
import random



def wordCloudChart(df):
    # делаем масску
    x, y = np.ogrid[:300, :400]
    mask = (x - 150) ** 2 + (y - 200) ** 2 > 200 ** 2
    mask = 255 * mask.astype(int)

    df_wc = df.groupby(['epithets'])[['epithets']].count()
    unique_words = df_wc.index.tolist()
    freqs = df_wc['epithets'].tolist()
    d = {w: f for w, f in zip(unique_words, freqs)}

    img = BytesIO()
    wc = WordCloud(background_color='white',
                   color_func=lambda *args, **kwargs: random.choice(["black"]),
                   min_font_size=5,
                   max_font_size=40,
                   prefer_horizontal=1,
                   mask=mask).fit_words(d)

    # переводим изображение в формат base64
    wc.to_image().save(img, format='PNG')
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())

