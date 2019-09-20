### 前言

上一章中我们学习了动画的初步，知道了如何移动一个物体，这一章我们来学习在界面上显示文字，同时还要学习一下如何播放声音，因为在游戏设计中，显示文字和播放音效是最基础的东西，对于`pygame`来说，处理这两者是比较容易的，这里用到两个包，分别是`pygame.font`和`pygame.mixer`。

### 显示文字

在`pygame`中，所有的元素均可当作`Surface`对象，这一点，在前一章创建动画的时候我们已经有接触，对于创建文字，同样需要这样处理，创建代码如下：

```python
fontObj = pygame.font.SysFont("simhei", 32)
```

这里我们直接调用了系统的字体，如果要看看当前系统中有哪些字体，`pygame`也给我们提供了相当方便的查询函数：

```python
In [2]: pygame.font.get_fonts()
Out[2]:        
['arial',      
 'arialblack', 
 'simsunnsimsun',
 'simsunextb',
 'symbol',
 'tahoma',
 'timesnewroman',
 'trebuchetms',
 'verdana',
 'webdings',
 'wingdings',
 'dengxian',
 'fangsong',
 'kaiti',
 'simhei',
 'holomdl2assets']
```

上图是自己电脑上已经安装的字体，如果我们想显示汉字，就需要选用一个汉字字体，否则程序会将汉字显示为方框，若要将文字显示在界面上，需要利用刚才我们创建的字体对象来添加文字，然后将该对象放在合适的位置上即可，这里要用到一个字体对象的方法`render`，该方法带有四个参数，第一个即是要添加的文字，第二个是布尔变量，显示是否反锯齿，第三个是文字的前景色，第四个是文字的背景色，示例代码如下：

```python
textSurfaceObj = fontObj.render("hello World", True, GREEN, WHITE)
```

然后根据这个字体对象得到其所对应的矩形框，然后再设置该矩形框的中心位置即可：

```python
textRectObj = textSurfaceObj.get_rect()
textRectObj.center = (300, 50)
```

当然为了将这文字显示在指定的屏幕上，需要在循环体内用`blit`函数进行复制：

```python
curSurface.blit(textSurfaceObj, textRectObj)
```

这样子，运行结果如下图所示：



用这种方法，我们来写一首诗，主要代码如下：

```python
poems = ['春眠不觉晓，','处处闻啼鸟。','夜来风雨声，','花落知多少。']
fontObj = pygame.font.SysFont("simhei", 50)
headTextObj = fontObj.render("春 晓", True, GREEN, BLUE)
headRectObj = headTextObj.get_rect()
headRectObj.center = (300, 50)

lstfont = []
count = 2
for i in poems:
    textSurfaceObj = fontObj.render(i, True, BLUE, WHITE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (300, 100*count)
    lstfont.append([textSurfaceObj, textRectObj])
    count += 1

while True:
    curSurface.fill(WHITE)
    curSurface.blit(textSurfaceObj, textRectObj)
    for iobj in lstfont:
        curSurface.blit(iobj[0], iobj[1])
    curSurface.blit(headTextObj, headRectObj)
```

运行图如下：



### 播放声音

这同样需要创建一个声音对象，代码如下：

```python
soundObj = pygame.mixer.Sound('sound/secosmic_lo.wav')
soundObj.play()
pygame.time.wait(1000)
soundObj.stop()
```

上述代码首先指定一个声音文件，然后播放，接着延时1秒后停止播放。在制作游戏的过程中，我们往往需要背景音乐，这时首先需要将背景音乐文件加载，代码如下：

```python
pygame.mixer.music.load('backgroundmusic.mp3')
pygame.mixer.music.play(-1, 0.0)
# ...在这里处理你的代码
pygame.mixer.music.stop()
```

要注意，`play`方法带两个参数，第1个参数为-1时，指的是循环播放，如果是其他数字的话，就是指播放的次数，第2个参数则是从声音文件的第几秒开始播放，有兴趣的同学可以实验一下，当然所有的声音文件是需要准备好放在程序能找到的位置处。



