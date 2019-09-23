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

### 响应键盘

处理键盘响应对于`pygame`来说也是相当简单的事情，只需要在循环体中对需要检测的键盘按键进行判断即可，比如我们用代码来响应`hello world`这两个单词，这里需要对`h`、`e`、`l`、`o`、`w`、`r`、`d`这七个字母进行判断，具体代码如下：

```python
    for event in pygame.event.get():
   		if event.type == KEYUP:
            if event.key in (K_h, K_e, K_l, K_o, K_w, K_r, K_d):
                print(event.key, chr(event.key))   
```

细心的同学可能注意到这里用`KEYUP`进行键盘响应检测，当程序发现键盘被按下后，立刻进入键盘检测状态，此时通过`event.key`来对用户的按键进行响应，要注意的是，这里获得的值是键盘按键对应的`unicode`编码，若需要将可打印的按键打印出来，则需要用`chr`函数进行相应的转换，运行截图如下：

