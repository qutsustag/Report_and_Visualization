
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 18:56:22 2022

@author: Trung Nguyen
"""

import time
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Frame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import rasterio
from matplotlib import pyplot
import matplotlib
matplotlib.use('TKAgg')
from rasterio.plot import show, show_hist
from PIL import Image
import pandas as pd
import os

###################-----------[INPUT]-------------#######################

pdf_name = 'pdf_template.pdf'
landsat_image = "landsat.NDVI.tif"
csv_filename = 'test_site_silk_exp20.csv'

title_text = "Research Computing Services"
title_text2 = "Plotting Geospatial Data with Python"
body_text = '''
Last month I wrote a blog post diving into the nitty gritty details about how to download a satellite image as a GeoTIFF file using Google’s Earth Engine API in Python. I also shared my code in this GitHub repo so that you all can use it freely. Over the past few weeks, I imagine that you’ve downloaded satellite imagery to your heart’s content, and now you may be wondering, “How can I plot my favorite geospatial dataset on top of this awesome satellite image using Python?” This blog post will help get you started toward answering that question.
'''
fig1_cap = "Figure 1: The Landsat imagery (left) and corresponding pixel histogram (right)"
fig2_cap = "Figure 2: Timeseries plot"


###################----------[END INPUT]----------#######################
#all inputs are of string type
#pdf_name: the name of pdf
#landsat_image: the filename including path of landsat image
#csv_filename: the filename inlcuding path of csv file


def pdf_gen(pdf_name, landsat_image, csv_filename,
 title_text, title_text2, body_text, fig1_cap, fig2_cap, add_border=True, clean_up=True):
    '''generic function to generate one-page report using reportlab'''

    #######################
    dataset = rasterio.open(landsat_image)
    fig, (ax1, ax2) = pyplot.subplots(1,2, figsize=(10,3), dpi=300)

    #ax1.ticklabel_format(style='plain')
    #ax2.ticklabel_format(style='plain')

    ret1 = show(dataset.read(1), transform=dataset.transform, ax = ax1, title = 'Landsat Imagery', cmap = 'BuGn')
    ret2 = show_hist(dataset.read(1), ax = ax2, title = 'Pixel Histogram', label = "Band 1")

    fig.colorbar(ret1.get_images()[0], ax = ax1)
    fig.text(0.5,-0.08, fig1_cap, ha = 'center')

    figure = pyplot.gcf()

    figure.set_size_inches(10, 3)
    pyplot.savefig('my_plot.png', dpi=300, bbox_inches = 'tight')

    ##########################

    df = pd.read_csv(csv_filename)

    #df.set_index('time', inplace = True)

    df = df[['time', 'somsc', 'aglivc', 'bglivcj', 'bglivcm']]

    fig = pyplot.figure(figsize=(10, 3))

    pyplot.plot(df.time, df.somsc, color='blue', label='somsc', 
            linewidth=3)
    pyplot.plot(df.time, df.aglivc, color='red', 
            label='aglivc', linewidth=3)
    pyplot.plot(df.time, df.bglivcj, color='green', 
            label='bglivcj', linewidth=3)
    pyplot.plot(df.time, df.bglivcm, color='purple', 
            label='bglivcm', linewidth=3)

    pyplot.title('Timeseries Plot')
    pyplot.xlabel('Time')
    pyplot.ylabel('Values')

    pyplot.legend()

    pyplot.tight_layout()

    fig.text(0.5,0,fig2_cap, ha = 'center')

    figure = pyplot.gcf()

    figure.set_size_inches(10, 5)
    pyplot.savefig("my_plot2.png", dpi=300, bbox_inches = 'tight')

    #################

    #set general pdf parameters

    pdf = canvas.Canvas(pdf_name)

    pdf.setPageSize(A4)

    pdf.setStrokeColor("BLUE")
    pdf.setLineWidth(0.5)

    
    #draw borders around pdf. Remove in the final product
    if add_border:
        pdf.line(72, 0, 72, 841)
        pdf.line(595-72, 0, 595-72, 841)
        pdf.line(0, 72, 595, 72)
        pdf.line(0, 841-72, 595, 841-72)


    ## Add Logo
    pdf.drawImage('logo.jpg', 500, 780, 50, 50)

    #define styles for text

    content1 = []

    content1.append(Spacer(1, 12))

    styles = getSampleStyleSheet()
    style1 = ParagraphStyle('Heading1',
                            parent=styles['Heading1'],
                            fontSize=16,
                            textColor = colors.black,
                            alignment = TA_CENTER)

    style2 = ParagraphStyle('Heading2',
                            parent=styles['Heading1'],
                            fontSize=15,
                            textColor = colors.purple,
                            leftIndent = 15,
                            rightIndent = 15,
                            alignment = TA_LEFT)

    style3 = ParagraphStyle('BodyText1',
                            parent=styles['Normal'],
                            fontSize=12,
                            textColor = colors.black,
                            leftIndent = 15,
                            rightIndent = 15,
                            alignment = TA_JUSTIFY)

    style4 = ParagraphStyle('FigureCaption',
                            parent=styles['Normal'],
                            fontSize=9,
                            textColor = colors.black,
                            alignment = TA_CENTER)

    #add pdf content
    #############


    ptext = Paragraph(title_text, style = style1)

    content1.append(ptext)

    #############

    content1.append(Spacer(1, 12))
    content1.append(Spacer(1, 12))

    #############


    ptext = Paragraph(title_text2, style = style2)

    content1.append(ptext)

    #############


    ptext = Paragraph(body_text, style = style3)

    content1.append(ptext)

    ##############

    #add figures in pdf 

    #pdf.drawImage(fig1, 95, 360, (595-95-95-20)/2, 180)

    #pdf.drawImage(fig2, ((595-95-95+20)/2)+95, 360, (595-95-95-20)/2, 180)
    fig4 = 'my_plot.png'
    im = Image.open(fig4)
    width, height = im.size

    pdf.drawImage(fig4, 85, 380, 425, 425*(height/width))
    im.close()
    
    
    fig5 = 'my_plot2.png'
    im = Image.open(fig5)
    width, height = im.size
    pdf.drawImage(fig5, 95, 140, 405, 425*(height/width))
    im.close()
    frame = Frame(72, 72, 595-72-72, 841-72-72)
    frame.addFromList(content1, pdf)
    

    #add figure captions in pdf

    ##############
    '''
    frame2 = Frame(115, 310, 150, 50)

    content2 = []


    ptext = Paragraph(fig1_cap, style = style4)

    content2.append(ptext)

    frame2.addFromList(content2, pdf)

    ##############

    frame3 = Frame(330, 310, 150, 50)

    content3 = []


    ptext = Paragraph(fig2_cap, style = style4)

    content3.append(ptext)

    frame3.addFromList(content3, pdf)

    ###############

    frame4 = Frame(230, 90, 150, 50)

    content4 = []


    ptext = Paragraph(fig3_cap, style = style4)

    content4.append(ptext)

    frame4.addFromList(content4, pdf)

    '''
    #generate pdf

    pdf.save()
    
    if clean_up:
        fig_list = [fig4, fig5]
        for fig in fig_list:
            os.remove(fig)

pdf_gen(pdf_name, landsat_image, csv_filename,
    title_text, title_text2, body_text, fig1_cap, fig2_cap, add_border=True, clean_up=True)