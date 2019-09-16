### 安装
关于`PyGame`的安装，如同`python`的第三方包一样，利用`pip`进行安装最为方便快捷：
```python
pip install pygame
```

在安装完成后，在`idle`中或是`ipython`等交互命令窗口利用以下代码可验证是成功：
```python
import pygame
```
如果上述代码没有报错，说明这个包已经成功安装，通常会打印出如下信息：
```python
pygame 1.9.6
Hello from the pygame community. https://www.pygame.org/contribute.html
```

### 动画基本框架
在介绍基本框架时，按照惯例，我们同样可用`hello world`来进行演示，代码如下：

```python
import pygame, sys
from pygame.locals import *

pygame.init()
DISPLAYSURF = pygame.display.set_mode((400, 300))
pygame.display.set_caption('hello world!')

while True: # main game loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
```

上述代码一共分为五部分：

1.  第一部分：导入

   ```python
   import pygame, sys
   from pygame.locals import *
   ```

   上述导入的第二行代码是因为`pygame.locals`中含有一些常量，比如上述代码中的`QUIT`，以这种方式导入后，在使用时比较方便。

2.  第二部分：初始化

   ```python
   pygame.init()
   ```

   这一句代码是所有采用`pygame`包开发的游戏都必须包含的。

3.  第三部分：设定舞台大小及标题等元素

   ```python
   DISPLAYSURF = pygame.display.set_mode((400, 300))
   pygame.display.set_caption('hello world!')
   ```

   这里是对游戏主窗口一些元素的设定，要注意的是`set_mode`函数接收的是一个`tuple`数据类型，并不是两个孤立的数，这一数对指定了要创建窗口的宽和高。当然`set_caption`顾名思意就是设置窗口的标题了。

4.  第四部分：事件循环

   ```python
   while True:
       for event in pygame.event.get():
           ...
   ```

   这是游戏的主循环，如果有同学仔细研究了上次的`PySimpleGUI`教程的话，会发现这种处理方式与那个创建窗体后响应事件的方式非常类似，不同的是这里用`pygame.event.get()`获取用户对窗口的所有响应。这里要注意，由于用户在同一时间有可能会对窗体进行多种操作，所以`pygame.event.get()`将返回一个列表，该列表中每一个元素均为`pygame.event.Event`类型，当然，如果用户不曾操作窗体，该列表将为空。

5.  第五部分：在事件循环中对相应的事件进行处理

   ```python
   if event.type == QUIT:
       pygame.quit()
       sys.exit()
   ```

   在窗体检测到“退出”指令的时候，程序将首先退出`pygame`，这里的`pygame.quit()`是和`pygame.init()`完全相反的一种状态，即对其内部创建的东西进行销毁，但程序本身仍然运行，所以还需要调用`sys.exit()`才能退出整个程序，当然在整个主循环过程中，为了保证窗体能实时刷新，需要显式调用以下代码：
   
   ```python
   pygame.display.update()
   ```
   
   如果将窗体主循环以图形来表示的话，下面这个简图可以很好地说明整个程序是如何执行的：

![loop](D:\思维导图\loop.png)

### 坐标系统

对于创建动画来说，研究其坐标系统当然是必须的，下面以一个8X8的界面来说明其坐标方向的规定：

![cor](D:\思维导图\cor.png)

从上图可以看出，`pygame`的坐标系统与电脑屏幕的坐标系统正常，与小海龟`turtle`的坐标是不一样的，有兴趣的同学可以查看前面的教程。

