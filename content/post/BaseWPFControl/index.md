---
title: 'WPF控件库 BaseWPFControl'
description: 从底层开始实现的WPF自定义控件库，包含基础控件和自定义控件
date: 2025-01-17T11:25:07+08:00
image: assets/cover.jpg
categories:
    - 项目

tags:
    - 前端
    - WPF
---

## 简介

`BaseWPFControl` 是一个 `dll`，基于 `.net 8.0` 和 `WPF` 框架实现，用于提供控件样式（包含基础控件和额外控件）。

## 基础控件

### Button

重写了基础控件 `Button` 的样式。

1. 新增 `BaseWPFControl:ButtonProperty.Icon` 附加属性用于提供按钮图标
2. 提供圆角

``` xml
<Button Content="纯文字按钮" Margin="10" />

<Button Content="图标" Margin="10" 
        BaseWPFControl:ButtonProperty.Icon="{StaticResource HomePage}" />

<Button Content="圆形按钮" Margin="10" 
        Style="{StaticResource CircleButtonStyle}" />

<Button Content="带图标的圆形按钮" Margin="10" 
        Style="{StaticResource CircleButtonStyle}" 
        BaseWPFControl:ButtonProperty.Icon="{StaticResource HomePage}" />

<Button Content="跑道形按钮" Margin="10" 
        Style="{StaticResource RoundButtonStyle}" />

<Button Content="图标" Margin="10" 
        Style="{StaticResource RoundButtonStyle}" 
        BaseWPFControl:ButtonProperty.Icon="{StaticResource HomePage}" />
```

![](assets/普通按钮-1748076976389-59.png)

针对不启用和不可点击的按钮，做出了区分，分别对应 `IsEnabled` 和 `IsHitTestVisible` 属性。

```xml
<Button Content="不启用" IsEnabled="False" Margin="10" />
<Button Content="不可点击" IsHitTestVisible="False" Margin="10" />
```
![](assets/Button区分不启用和不可点击-1748076976389-60.png)

之所以这样去做目的是为了 `GPIO` 的控制，`GPI` 不可点击，`GPO` 可点击。

提供了两种相似的样式 `BooleanStateButtonStyle` 和 `BooleanToggleButtonStyle`。前者对应于 `GPI`，不可点击，仅用于展示 `GPI` 状态，后者对应于 `GPO`，既可以展示 `GPO` 状态，又可以通过点击切换状态。

```xml
<Button Style="{StaticResource BooleanStateButtonStyle}" Margin="10" 
        Tag="{Binding State}" />
<Button Style="{StaticResource BooleanToggleButtonStyle}" Margin="10"
        Tag="{Binding State}" Command="{Binding ChangeStateCommand}" />
```
![](assets/ButtonStateToggle关闭-1748076976389-61.png)

![](assets/ButtonStateToggle开启-1748076976389-64.png)

### ToggleButton

基于 `ToggleButton` 重写样式，该控件的本意是用于 `GPIO` 的控制

```xml
<ToggleButton IsChecked="{Binding State}" Margin="10" />

<ToggleButton IsChecked="{Binding State}" Margin="10" IsEnabled="False" />
```

![](assets/ToggleButton关闭-1748076976389-62.png)

![](assets/ToggleButton开启-1748076976389-63.png)

> 最终方案如下：
> - `GPI` 使用 `Button` 的 `BooleanStateButtonStyle` 样式
> - `GPO` 使用 `ToggleButton` 的默认样式。

### RadioButton

重写 RadioButton 的样式，主要优化如下：
1. 勾选后样式变化
2. 勾选框尺寸跟随字体尺寸变化

``` xml
<RadioButton Content="未勾选" />
<RadioButton Content="勾选" IsChecked="True" />
<RadioButton Content="未勾选未启用" IsEnabled="False" IsChecked="False" />
<RadioButton Content="勾选未启用" IsEnabled="False" IsChecked="True"  />
<RadioButton Content="大字体" FontSize="30" />
```
![](assets/RadioButton-1748076976389-65.png)

### CheckBox

重写 CheckBox 的样式，主要优化如下：
1. 勾选后样式变化
2. 勾选框圆角
3. 勾选框尺寸跟随字体尺寸变化

``` xml
<CheckBox Content="未勾选" />
<CheckBox Content="勾选" IsChecked="True" />
<CheckBox Content="未勾选未启用" IsEnabled="False" IsChecked="False" />
<CheckBox Content="勾选未启用" IsEnabled="False" IsChecked="True" />
<CheckBox Content="大字体" FontSize="30" />
```

![](assets/CheckBox-1748076976389-68.png)

### ComboBox

重写 ComboBox 样式，主要优化如下：
1. 圆角属性
2. 提供 ComboBox 绑定枚举值的扩展语法 EnumBindingSource

```xml

<!--示例1：ComboBox绑定枚举值-->
<ComboBox Margin="10" Width="120"
          ItemsSource="{BaseWPFControl:EnumBindingSource 
                                        EnumType=BaseTest:EnumDayOfWeek}"
          SelectedItem="{Binding SelectedEnumDayOfWeek}" >
    <ComboBox.ItemTemplate>
        <DataTemplate>
            <TextBlock Text="{Binding 
                       Converter={StaticResource EnumToDescriptionConverter}, 
                       Mode=OneWay}" />
        </DataTemplate>
    </ComboBox.ItemTemplate>
</ComboBox>

<!--示例2：不启用ComboBox-->
<ComboBox Margin="10" Width="120" IsEnabled="False" >
    <ComboBoxItem Content="1" IsSelected="True" />
</ComboBox>

<!--示例3：ComboBox绑定字典-->
<!--note：需要设置 DisplayMemberPath 和 SelectedValuePath，-->
<!--note：并只能使用 SelectedValue 进行访问-->
<ComboBox Margin="10" Width="120" ItemsSource="{Binding DictionaryDayOfWeek}"
          DisplayMemberPath="Value" SelectedValuePath="Key"
          SelectedValue="{Binding SelectedDictionaryDayOfWeek}" />

<!--示例4：ComboBox绑定列表-->
<!--note：使用 SelectedItem 或者 SelectedValue 都可以获得正确结果-->
<!--note: 前提是绑定的值在列表中，也可以通过 SelectedIndex 进行访问-->
<ComboBox Margin="10" Width="120" ItemsSource="{Binding ListDayOfWeek}"
          SelectedItem="{Binding SelectedListDayOfWeek}" />

```

![](assets/ComboBox-1748076976389-66.png)

### TextBlock

重写 `TextBlock` 的样式，主要优化如下：
1. 中英文使用不同的字体显示，中文使用`微软雅黑`，英文使用`Consolas`

```xml
<TextBlock Text="显示中文" Margin="10" />
<TextBlock Text="Show English" Margin="10" />
```

![](assets/TextBlock-1748076976389-69.png)

### MemoryBlock

该控件为自定义控件，主要实现以下功能：

1. 获取当前软件已使用内存，以 `MB` 为单位
2. 可以通过控件的 `Interval` 属性设置更新频率，单位为 `ms`，默认为 `1000 ms`
3. 可以通过控件的 `Header` 属性设置前缀文字
3. 可以通过控件的 `UsedMemory` 只读属性获取内存

```xml
<BaseWPFControl:MemoryBlock Margin="10" />
```

![](assets/MemoryBlock-1748076976389-67.png)

### LogBlock

该控件为自定义控件，配合 `BaseLogManager` 一起使用，主要实现以下功能：

1. 显示日志
2. 提供日志详情页

```xml
<BaseWPFControl:LogBlock x:Name="LogBlock_Test" />

<ContentControl Height="400" Margin="10"
                Content="{Binding ElementName=LogBlock_Test, Path=LogView}" />
```

![](assets/LogBlock-1748076976389-70.png)

### TextBox

重写 `TextBox` 的样式，主要实现以下功能：

1. 可以通过 `TextBoxProperty.Prefix` 属性设置前缀文字
2. 可以通过 `TextBoxProperty.WaterMask` 属性设置水印文字
3. 可以通过 `TextBoxProperty.Suffix` 属性设置后缀文字
4. 输入时边框高亮显示
5. 大文本输入框可以通过滚动条上下滚动

```xml
<TextBox Width="200"  Margin="10" 
         BaseWPFControl:TextBoxProperty.Prefix="www." 
         BaseWPFControl:TextBoxProperty.Suffix=".com"
         BaseWPFControl:TextBoxProperty.WaterMask="输入网址" />
<TextBox Width="160" Margin="10" Text="默认文本框" />
<TextBox Width="100" Margin="10" 
         BaseWPFControl:TextBoxProperty.WaterMask="绑定Decimal类型"
         Text="{Binding DecimalNumber, StringFormat=0.#}" />

<TextBox Style="{StaticResource BigTextBox}" 
         Width="400" Height="100" Margin="10" Text="{Binding Poetry1}" />
```

![](assets/TextBox-1748076976389-75.png)

![](assets/BitTextBox-1748076976389-71.png)

### NumericBox

`NumericBox` 为自定义控件，主要实现以下功能：

1. 更方便的绑定数字，并提供限制
2. 可以通过 `Value` 属性获取/设置值
3. 可以通过 `TextFormat` 属性设置文本格式
4. 可以通过 `MinValue` 属性设置最小值
5. 可以通过 `MaxValue` 属性设置最大值
6. 可以通过 `Interval` 属性设置点击增减按钮时的变化量
7. 可以通过 `ValueChanged` 事件获取值改变事件

```xml
<BaseWPFControl:NumericBox Value="{Binding DecimalNumber}" TextFormat="0.#" 
                           MinValue = "0" MaxValue = "100" Interval = "1"
                           ValueChanged="NumericBox_ValueChanged" />
<BaseWPFControl:NumericBox Value="{Binding DecimalNumber}" TextFormat="0.#" 
                           IsEnabled="False" />
```

![](assets/NumericBox-1748076976389-72.png)

### PasswordBox

重写 `PasswordBox` 样式，主要实现以下功能：
1. 可以通过 `PasswordBoxProperty.CanShowPassword` 属性设置是否显示密码的功能

```xml
<PasswordBox Width="200" Margin="10" Password="123456" />
<PasswordBox Width="200" Margin="10" Password="123456" 
             BaseWPFControl:PasswordBoxProperty.CanShowPassword="False" />
```

![](assets/PasswordBox-1748076976389-73.png)

### DatePicker & DateTimePicker

`DatePicker` 和 `DateTimePicker` 都是自定义控件，主要实现以下功能：
1. 选择时间和日期，这两个控件的区别在于一个前者只有日期，后者包含时间
2. 可以通过 `SelectedDateTime` 获取选中的日期时间
3. 可以通过 `SelectedDateTimeFormat` 设置日期时间的格式
4. 可以通过 `SelectedDateTimeChanged` 获取时间改变的事件

```xml
<BaseWPFControl:DatePicker Margin="10" />
<BaseWPFControl:DateTimePicker Margin="10" />
```
![](assets/DateTimePicker-1748076976389-74.png)

### SelectFileBlock & SelectFolderBlock

`SelectFileBlock` 和 `SelectFolderBlock` 都是自定义控件，主要实现以下功能：
1. 点击按钮通过对话框选择文件或者文件夹
2. 可以通过 `SelectedPath` 属性获取/设置路径
3. 可以通过 `SelectedPathChanged` 获取选中路径改变的事件
4. `SelectFileBlock` 可以通过 `ExtensionFilter` 属性设置文件过滤
5. 鼠标移动到文字上方出现 `ToolTip` 显示路径的全文
6. 鼠标双击文字直接跳转到路径所在的文件夹

![](assets/SelectFileBlock-1748076976389-76.png)

### Image

提供一些内置的 `SVG`，可以直接通过 `Source` 绑定 `StaticResource` 值进行设置

```xml
<Image Source="{StaticResource DirectoryConfig}" Height="50" Margin="10" />
```

![](assets/SVGImage-1748076976389-77.png)

### ProgressBar & Loading

1. 重写 `ProgressBar` 样式，提供圆角
2. 可以通过 `ProgressBarProperty.ShowValue` 属性设置进度条显示当前值
3. 提供扩展函数 `SetAnimateValue` 设置进度条的值，通过该函数设置可以显示动画
4. 提供自定义控件圆形进度条 `Loading`，仅用于等待功能

```xml
<ProgressBar Height="40" Width="400" d:Value="20"/>
<ProgressBar Height="40" Width="400" IsIndeterminate="True"/>
<BaseWPFControl:Loading Diameter="150" StrokeThickness="30" 
                        Content="加载中，请等待..." />
```

![](assets/ProgressBar-1748076976389-78.png)

### Clock & Calendar

1. 重写 `Calender` 样式
2. 提供 自定义控件 `Clock`，用于选择时间

```xml
<Calendar x:Name = "Calendar" />

<BaseWPFControl:Clock Height="{Binding ActualHeight, ElementName=Calender}"/>
```

![](assets/Calender-1748076976389-79.png)

### TabControl

重写 `TabControl` 的样式

```xml
<TabControl TabStripPlacement="Left">
    <TabItem Header="水调歌头" >
        <TextBlock Text="{Binding Poetry1}" FontSize="14" />
    </TabItem>
    <TabItem Header="如梦令" >
        <TextBlock Text="{Binding Poetry2}" FontSize="14" />
    </TabItem>
    <TabItem Header="破阵子" >
        <TextBlock Text="{Binding Poetry3}" FontSize="14" />
    </TabItem>
    <TabItem Header="未启用" IsEnabled="False" />
</TabControl>
```

![](assets/TabControl-1748076976389-80.png)

## 复杂控件

### ConfigControl

提供自定义控件 `ConfigControl`，用于方便的实现配置界面

```xml
<BaseWPFControl:ConfigControl ConfigName="日期时间">
    <BaseWPFControl:DateTimePicker />
</BaseWPFControl:ConfigControl>

<BaseWPFControl:ConfigControl ConfigName="选择文件">
    <BaseWPFControl:SelectFileBlock Width="280" />
</BaseWPFControl:ConfigControl>
```

![](assets/ConfigControl-1748076976389-81.png)

### LisBox

重写 `ListBox` 的样式，可以绑定 `Enum/List/Dictionary`

![](assets/ListBox-1748076976389-82.png)

### ListView

1. 重写 `ListView` 的样式

![](assets/ListView-1748076976389-83.png)

### DataGrid

重写 `DataGrid` 的样式，这里包含两种样式，一种是选择单元格，另一种是鼠标经过选中整行

![选中单元格](assets/DataGrid-1748076976389-84.png)
![无法选中，鼠标经过选中整行](assets/ListViewDataGrid-1748076976389-85.png)

## 更新记录

更新了部分 `BaseWPFControl` 中的控件，实现了更多的功能。

### 优化`ListBox`

实际使用了一下`ListBox`之后发现还是有很多问题，尤其是关于调整属性之后，并且给出了更多的示例

![](assets/PixPin_2025-03-17_10-07-54-1748075157664-1-1748076976389-86.png)

### 新增`BaseClipBorder`

- 实现了新的控件`BaseClipBorder`来解决边框溢出和边框圆角缝隙的问题
- 最终实现如右图所示

![](assets/PixPin_2025-03-26_20-07-25-1748075157664-4-1748076976389-87.png)

### 优化ProgressBar

- 在上面`BaseClipBorder`的基础上优化了`ProgressBar`的实现
- 给出了垂直`ProgressBar`例程实现

![](assets/PixPin_2025-03-26_20-10-51-1748075157664-3-1748076976389-88.gif)

### 新增`DefaultControlStyle`和`DefaultWindowStyle`

这样设计的原因其实是为了移除掉`TextBlock`的`FontSize`属性和`FontFamily`属性，改为直接从`Window`或者`UserControl`中继承字体属性。

而`DefaultControlStyle`中定义了基础的`FontSize`和`FontFamily`样式，并且任何控件都可以使用。

### 优化`Button`

- 删除了关于`ButtonShape`属性的内容
- 新增了一些无边框按钮的样式
- 统一了`BorderBrush`和`BorderThickness`的风格

![](assets/PixPin_2025-03-26_20-04-46-1748075157664-2-1748076976389-89.png)

### 优化`ComboBox`

- 重写了`ComboBox`的样式
- 新增`ComboBoxItem`的样式

![](assets/PixPin_2025-03-26_20-15-22-1748075157664-5-1748076976389-90.png)
![](assets/PixPin_2025-03-26_20-15-01-1748075157664-6-1748076976390-99.png)

### 新增`InnerSeparator`属性

- 新增`BaseWPFControl:ControlProperty.InnerSeparator`属性，一般用于内部存在间隙属性调整

```Markdown
<Button Content="图标" Margin="10" 
        BaseWPFControl:ButtonProperty.Icon="{StaticResource HomePage}"
        BaseWPFControl:ControlProperty.InnerSeparator="20" />
```

![](assets/PixPin_2025-03-26_20-34-49-1748075157665-7-1748076976390-92.png)

### 优化`DataGrid`

在使用`DataGrid`的时候，我发现有些属性没有效果，或者不尽如人意。

所以我就重新整理了一下`DataGrid`的实现，并且给出了详细的案例。

![](assets/PixPin_2025-03-28_09-40-06-1748075157665-8-1748076976390-98.png)
![](assets/PixPin_2025-03-28_09-41-09-1748075157665-10-1748076976389-91.png)
![](assets/PixPin_2025-03-28_09-41-14-1748075157665-9-1748076976390-93.png)

### 优化`Calendar`和`Clock`

![](assets/PixPin_2025-03-28_13-59-15-1748075157665-11-1748076976390-94.png)

### 优化`FlipBox`

![](assets/PixPin_2025-03-28_13-59-39-1748075157665-12-1748076976390-95.png)

### 新增`Dialog`显示成`Window`

可以调用`ShowDialogAsWindow`函数，将`Dialog`显示成独立的`Window`，就算没有`DialogContainer`也能显示。使用体验和`WPF`原生的`ShowDialog`函数类似。

![](assets/PixPin_2025-03-28_14-07-45-1748075157665-13-1748076976390-96.png)
![](assets/PixPin_2025-03-28_14-07-37-1748075157665-14-1748076976390-97.png)

### 优化`ListBox`

和之前的显示一致，只是使用`BaseClipBorder`简化了内部实现。

![](assets/PixPin_2025-03-28_14-21-24-1748075157665-15-1748076976390-101.png)

### 优化`ListView`

![](assets/PixPin_2025-03-28_16-19-43-1748075157665-16-1748076976390-102.png)

### 优化`SmoothProgress`

这里省事，直接让`SmoothProgressBar`使用`ProgressBar`的样式

![](assets/PixPin_2025-03-28_17-44-38-1748075157665-18-1748076976390-100.png)

### 新增`SimpleScrollViewer`样式

- 该样式没有滚动条，只有箭头按钮，并且增加了滚动动画
- 主要用于`TabControl`的`Header`部分

![](assets/PixPin_2025-04-02_11-18-51-1748075157665-17-1748076976392-103.png)

### 优化`TabControl`

- 优化了微软原生样式下，`TabItem`溢出的问题

![](assets/PixPin_2025-04-02_11-19-13-1748075157665-19-1748076976392-104.png)
