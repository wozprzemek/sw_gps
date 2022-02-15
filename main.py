import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def animate(i):
    data = pd.read_csv('data.csv')
    longitude = data['longitude']
    latitude = data['latitude']

    # BBox = ((longitude.min(), longitude.max(),
    #          latitude.min(), latitude.max()))
    BBox = ((16.96219, 16.9641902,
             52.39918, 52.40143))

    ruh_m = plt.imread(r'/Users/leskyy/PycharmProjects/positionPloting/map.png')
    plt.cla()
    plt.scatter(longitude, latitude, zorder=1, alpha=1, c='g', s=50)
    plt.xlim(BBox[0], BBox[1])
    plt.ylim(BBox[2], BBox[3])
    plt.imshow(ruh_m, zorder=0, extent=BBox, aspect='equal')

    plt.plot(longitude, latitude)


ani = FuncAnimation(plt.gcf(), animate, interval=1000)
plt.show()
