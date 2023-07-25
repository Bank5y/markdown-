# Markdown本地转换

## 功能

用于处理Markdown文件（.md）。它可以自动下载Markdown文件中引用的图片和音频，并将这些资源保存到本地，同时在Markdown文件中使用相对地址替换原始网络地址。此外，程序还提供了筛选功能，可以标记已处理过的文件，并在后续运行时跳过这些文件，以避免重复处理。

## 说明

转换仅适用于在md文件中使用html的audio标签插入的音频和img标签插入的图片

为什么不能支持其他形式的图片音频或者视频?因为本质上这个本地转换是另一个脚本的扩展,仅仅只用于转换特定格式的网络资源

原脚本地址:[Li-Weijian/GeekTimeSpider: 极客时间专栏文章爬取 (github.com)](https://github.com/Li-Weijian/GeekTimeSpider)

## 可调参数

在程序中，可以设置以下可调参数：

1. `scan_option`：设置扫描选项，可选值为 `'root'` 或 `'sub'`。当值为 `'root'` 时，程序只会扫描当前文件夹下的Markdown文件；当值为 `'sub'` 时，程序会递归扫描当前目录及其子目录下的Markdown文件。

## 使用方法

1. 确保程序文件 `md.py` 与待处理的Markdown文件（.md）位于同一目录。

2. 打开终端或命令行窗口，进入到程序文件所在的目录。

3. 运行程序：

   ```cmd
   python md.py
   ```

4. 程序会自动处理Markdown文件中引用的图片和音频，将资源下载到本地的对应文件夹中，并在Markdown文件中使用相对地址替换原始网络地址。

5. 运行完成后，会在当前目录下生成 `finish.txt` 文件，其中记录已处理过的文件名。

## 需要安装的运行环境和包

为了运行这个程序，你需要安装以下环境和包：

1. Python 3.x：确保你的系统中已经安装了Python 3.x版本。

2. tqdm 包：这个包用于在终端中显示进度条。你可以使用以下命令安装该包：

   ```cmd
   pip install tqdm
   ```

## `finish.txt` 和 `run.log` 的介绍

1. `finish.txt`：这个文件用于记录已处理过的文件名。每当处理完一个Markdown文件时，程序会将文件名写入 `finish.txt` 中，以便后续运行时可以跳过这些文件。
2. `run.log`：这是运行日志文件，用于记录程序运行时的信息。包括文件处理的开始时间、完成时间以及报错信息（如果有的话）。你可以查看此文件来了解程序运行的详细情况。

**注意：** 请确保在运行程序时，Markdown文件和程序文件位于同一目录，并按照程序功能介绍中的方法设置好可调参数。