### pygame教程（2）：绘制几何图形

---

### 前言

在上一章中，我们学习了利用`pygame`创建程序的基本框架、坐标系统以及颜色和区域的设定等基本元素，这一章中，主要利用`pygame`的一些主要绘图函数绘制一些常见的几何图形，有兴趣的同学可以将这种绘图方式与小海龟`turtle`进行比较，看有什么区别。

### 绘图

先来放一张绘图效果看看：

![Drawing_001](/home/iefan/Pictures/Drawing_001.png)

如果仔细学习过小海龟`turtle`的同学们应该也能画出如上图形，但如果研究一下`pygame`的代码，将会发现在这里，绘制这些图形都非常容易，下面展示了绘制图形的一些主要代码：

```python
pygame.draw.polygon(curSurface, GREEN, ((146,0), (291, 106), (236, 277), (56,277), (0, 106)))
pygame.draw.line(curSurface, BLUE, (60, 60), (120, 60), 4)
pygame.draw.line(curSurface, BLUE, (120, 60), (60, 120))
pygame.draw.line(curSurface, BLUE, (60, 120), (120, 120), 4)
pygame.draw.circle(curSurface, BLUE, (300,50), 30, 11)
pygame.draw.circle(curSurface, BLUE, (250,300), 30, 0)
pygame.draw.ellipse(curSurface, RED, (300, 250, 40, 80), 1)
pygame.draw.rect(curSurface, RED, (200, 150, 100, 50))
```

这八行代码绘制了八个图形，熟悉英文的同学当然很容易从名称上看得出来，下面列表展示了这几个函数的具体用法：

| 功能   | 函数                                                         | 描述                                                         |
| ------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 多边形 | pygame.draw.polygon(surface, color, pointlist, width)        | 第1个参数指定屏幕，第2个参数指定颜色，第3个参数指定多边形各顶点的坐标集合，第4个参数确定该多边形的边宽。 |
| 线段   | pygame.draw.line(surface, color, start_point, end_point, width) | 第1个参数指定屏幕，第2个参数指定颜色，第3、第4个参数指定该线段的起止点，第5个参数指定线宽。 |
| 折线   | pygame.draw.lines(surface, color, closed, pointlist, width)  | 第1个参数指定屏幕，第2个参数指定颜色，第3个参数指定折线是否闭合，第4个参数是一系列点的集合，第5个参数指定线宽。 |
| 圆     | pygame.draw.circle(surface, color, center_point, radius, width) | 第1个参数指定屏幕，第2个参数指定颜色，第3个参数指定圆心，第4个参数指定半径，第5个参数指定圆环的厚度，若为0，则绘制出整个圆。 |
| 椭圆   | pygame.draw.ellipse(surface, color, bounding_rectangle, width) | 第1个参数指定屏幕，第2个参数指定颜色，第3个参数指定一个长方形，第4个参数指定线宽，若为0，则绘制整个椭圆并填充。 |
| 长方形 | pygame.draw.rect(surface, color, rectangle_tuple, width)     | 第1个参数指定屏幕，第2个参数指定颜色，第3个参数指定长方形两个顶点坐标及宽高数据，第4个参数指定矩形宽度，若为0，绘制整个矩形。 |

### 关于描点

如果比较细心的同学观察上图，会发现在这张图的右下角有5个黑点，在`pygame.draw`类中，并没有提供描点的函数，不过为了实现这一功能，当然可以用`pygame.draw.line`进行绘制，但是由于`pygame`的某种机制，这样的运行速度很慢，所以可以采用`pygame.PixelArray`对象来实现这一功能。

具体代码如下：

```python
pixObj = pygame.PixelArray(curSurface)
pixObj[480][380] = BLACK
pixObj[482][382] = BLACK
pixObj[484][384] = BLACK
pixObj[486][386] = BLACK
pixObj[488][388] = BLACK
del pixObj
```

需要说明的是，在创建了`pygame.PixelArray`对象后，便可以用该对象完全操纵当前界面上的每一个像素点，但要注意的是，在这些点的颜色设置完成后，需要调用`del pixObj`来对屏幕完成**解锁**操作，因为在创建了该像素数组后，整个屏幕要进行锁定，这可以用`curSurface.get_locked()`函数查询是否锁定，在屏幕锁定时，如果调用函数`blit`进行图像的移动，程序就会报错，所以在设置完成后，最好将该数组删除以便于屏幕解锁。

### 绘制弧形

`pygame`提供了绘制弧形的函数，使用起来要稍加注意，因为弧形只是圆形的一部分，所以要使用弧度，这里需要引入一个`math`的包，主要使用其中的`pi`值。

函数说明如下：

| 功能     | 函数                                                        | 描述                                                         |
| -------- | ----------------------------------------------------------- | ------------------------------------------------------------ |
| 绘制弧形 | arc(Surface, color, Rect, start_angle, stop_angle, width=1) | 第1个参数指定屏幕，第2个参数指定颜色，第3个参数是一个矩形，第4个参数指定起始角度，第5个参数指定终止角度，第6个参数指定线宽 |

例子代码：

```python
pygame.draw.arc(curSurface, BLACK, (100, 40, 340, 340), 0, math.pi, 1)
pygame.draw.arc(curSurface, BLUE, (100, 200, 340, 150), math.pi, 2*math.pi, 1)
```

绘制图如下：



### 反锯齿问题

在屏幕上绘制曲线，由于是对不同的像素进行着色，而像素的排列是规整有序的，于是当绘制斜线的时候，锯齿问题就比较突出，`pygame`本身提供了两个函数来绘制反锯齿线，其使用方法与常规的线段绘制方法相同，区别在于反锯齿线只能绘制单像素宽的线，演示代码如下：

```python
pygame.draw.lines(curSurface, RED, False, ((146,0), (291, 106), (236, 277)))
pygame.draw.aalines(curSurface, BLUE, False, ((140,0), (280, 106), (226, 277)))

pygame.draw.line(curSurface, RED, (150,80), (300,300))
pygame.draw.aaline(curSurface, BLUE, (100,100), (300,300))
```

绘制比较图如下所示：



从图上可以看出，蓝色为反锯齿线，红色为普通线，很明显红色线条能看出锯齿样。