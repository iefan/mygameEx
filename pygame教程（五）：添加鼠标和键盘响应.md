### 前言

上一章中我们学习了如何为游戏添加文字和声音，这一章我们来研究一下如何响应鼠标和键盘。在学习`turtle`时，为了响应鼠标的点击，我们必须借用`tkinter`的功能，在`pygame`中响应鼠标和键盘是非常简单的行为。

### 响应鼠标

鼠标点击或移动对于程序而言都只是一个普通事件，只需要在循环体`while`中对`event.type`进行判断即可，具体代码如下：

```python
    for event in pygame.event.get():
		if event.type == MOUSEBUTTONUP:
            mouse_x, mouse_y = event.pos
            print(mouse_x, mouse_y)

```

这段代码即可检测鼠标是否按下，并返回鼠标点击的位置，从处理方式来看，这要比`turtle`简单很多。

我们来做一段小程序，它将完成这样的功能：在一个界面上有一些图标，它们被整齐地排列着，当用户点击任意一个图标时，控制台上打印出该图标所在的列和行。

代码如下：

```python
#...... 其它代码

def findBlockByPos(mouse_x, mouse_y):
    for i in range(m):
        for j in range(n):
            if mouse_x > lstBlockRect[i][j][0] and mouse_x <= lstBlockRect[i][j][0] + blockWidth:
                if mouse_y > lstBlockRect[i][j][1] and mouse_y <= lstBlockRect[i][j][1] + blockWidth:
                    print("pos", i, j)
                    
while True:
    mouse_x,mouse_y = -1,-1
    drawBackGround() ## 绘制背景
    drawIcon()       ## 绘制图标
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONUP:
            mouse_x, mouse_y = event.pos
    findBlockByPos(mouse_x, mouse_y)
    pygame.display.update()
```

上述代码可以实现查找图标位置的功能，利用鼠标点击时所得到的坐标，将其与各个图标所在的位置进行比较，如果点击位置位于图标所在位置，即将该处图标的列与行打印出来即可。这段代码是一个小游戏的代码片段，实际运行效果如下所示：



### 响应键盘

处理键盘响应对于`pygame`来说也是相当简单的事情，只需要在循环体中对需要检测的键盘按键进行判断即可，比如我们用代码来响应`hello world`这两个单词，这里需要对`h`、`e`、`l`、`o`、`w`、`r`、`d`这七个字母进行判断，具体代码如下：

```python
    for event in pygame.event.get():
   		if event.type == KEYUP:
            if event.key in (K_h, K_e, K_l, K_o, K_w, K_r, K_d):
                print(event.key, chr(event.key))   
```

细心的同学可能注意到这里用`KEYUP`进行键盘响应检测，当程序发现键盘被按下后，立刻进入键盘检测状态，此时通过`event.key`来对用户的按键进行响应，要注意的是，这里获得的值是键盘按键对应的`unicode`编码，若需要将可打印的按键打印出来，则需要用`chr`函数进行相应的转换，运行截图如下：

可能有的同学会想问如果要输入大写字母怎么办？其实也很简单，只需要判断用户在按下按键时是否有同时将`shift`一起按下，判断是否组合按键输入的方法是用`pygame.key.get_mods`函数来检测，代码如下：

```python
if event.type == KEYUP:
	if event.key in (K_h, K_e, K_l, K_o, K_w, K_r, K_d):
		if pygame.key.get_mods():
			print(event.key, chr(event.key).upper())
		else:
			print(event.key, chr(event.key))
```

以上代码可以检测用户的大小写输入。

当然有的同学会问，如果不用`shift`加字母来输出大写，那么是否可以将`capslock`按钮点亮来输入大写字母呢，回答当然是可以的，此时`pygame.key.get_mods()`返回`8192`这个值。

但是在按下`capslock`这个按钮时，再按`shift`与字母的组合键，`pygame.key.get_mods()`将返回`8193`这个值，为了统一输出，需要将代码修正为如下：

```python
if event.type == KEYUP:
    if event.key in (K_h, K_e, K_l, K_o, K_w, K_r, K_d):
        if pygame.key.get_mods() in (1, 8192):
            print(event.key, chr(event.key).upper())
        else:
            print(event.key, chr(event.key))
```

输出结果如图：

