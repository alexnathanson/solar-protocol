#######################################################################
###                                                        LIBRARIES                                                            ###
#######################################################################
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#######################################################################
###                                                    HELPER FUNCTIONS                                                ###
#######################################################################

#USE: Create an array structure for rings.
#INPUT: a df of row length 1 with the first column as the current metric value and the second colum is the target metric value
#OUTPUT: an aray of arrays representing each ring
def calculate_rings(df):
  if df.iloc[0,0] < df.iloc[0,1]:
    rings=[[df.iloc[0,0],df.iloc[0,1]-df.iloc[0,0]],[0,0]]
  elif df.iloc[0,0] / df.iloc[0,1] < 2:
    rings=[[df.iloc[0,0],0],[df.iloc[0,0] % df.iloc[0,1], df.iloc[0,1]-df.iloc[0,0] % df.iloc[0,1]]]
  else:
    rings = [[0,0],[0,0]]
  return rings

#USE: Determine if the label for the rotating number label should be left/center/right
#INPUT: a df of row length 1 with the first column as the current metric value and the second colum is the target metric value
#OUTPUT: the proper text alignment
def horizontal_aligner(df):
  metric = 1.0 * df.iloc[0,0] % df.iloc[0,1] / df.iloc[0,1]
  if metric in (0, 0.5):
    align = 'center'
  elif metric < 0.5:
    align = 'left'
  else:
    align = 'right'
  return align

def vertical_aligner(df):
  metric = 1.0 * df.iloc[0,0] % df.iloc[0,1] / df.iloc[0,1]
  if metric < 0.25:
    align = 'bottom'
  elif metric < 0.75:
    align = 'top'
  elif metric > 0.75:
    align = 'bottom'
  else:
    align = 'center'
  return align

#USE: Create a center label in the middle of the radial chart.
#INPUT: a df of row length 1 with the first column as the current metric value and the second column is the target metric value
#OUTPUT: the proper text label
def add_center_label(df):
    percent = str(round(1.0*df.iloc[0, 0]/df.iloc[0, 1]*100,1)) + '%'
    return plt.text(0,
           0.2,
           percent,
           horizontalalignment='center',
           verticalalignment='center',
           fontsize = 40,
           family = 'sans-serif')

#USE: Formats a number with the apropiate currency tags.
#INPUT: a currency number
#OUTPUT: the properly formmated currency string
def get_currency_label(num):
  currency = ''
  if num < 10**3:
    currency = '$' + str(num)
  elif num < 10**6:
      currency = '$' + str(round(1.0*num/10**3,1)) + 'K'
  elif df.iloc[0,0] < 10**9:
    currency = '$' + str(round(num/10**6,1)) + 'M'
  else:
    currency = '$' + str(round(num/10**9,1)) + 'B'

  return currency

#USE: Create a dynamic outer label that servers a pointer on the ring.
#INPUT: a df of row length 1 with the first column as the current metric value and the second column is the target metric value
#OUTPUT: the proper text label at the apropiate position
def add_current_label(df):
  currency = get_currency_label(df.iloc[0,0])
  print('vertical: ' + vertical_aligner(df))
  print('horizontal: ' + horizontal_aligner(df))
  return plt.text(1.5 * np.cos(0.5 *np.pi - 2 * np.pi * (float(df.iloc[0,0]) % df.iloc[0,1] /df.iloc[0,1])),
           1.5 * np.sin(0.5 *np.pi - 2 * np.pi * (float(df.iloc[0,0]) % df.iloc[0,1] / df.iloc[0,1])),
                  currency,
                  horizontalalignment=horizontal_aligner(df),
                  verticalalignment=vertical_aligner(df),
                  fontsize = 20,
                  family = 'sans-serif')

def add_sub_center_label(df):
    amount = 'Goal: ' + get_currency_label(df.iloc[0,1])
    return plt.text(0,
            -.1,
            amount,
            horizontalalignment='center',
            verticalalignment='top',
            fontsize = 22,family = 'sans-serif')

#######################################################################
###                                                    MAIN FUNCTION                                                        ###
#######################################################################

def create_radial_chart(df, color_theme = 'Purple'):

# base styling logic
  color = plt.get_cmap(color_theme + 's')
  ring_width = 0.3
  outer_radius = 1.5
  inner_radius = outer_radius - ring_width

  # set up plot
  ring_arrays = calculate_rings(df)
  fig, ax = plt.subplots()

  if df.iloc[0, 0] > df.iloc[0, 1]:
    ring_to_label = 0
    outer_edge_color = None
    inner_edge_color = 'white'
  else:
    ring_to_label = 1
    outer_edge_color, inner_edge_color = ['white', None]

  # plot logic
  outer_ring, _ = ax.pie(ring_arrays[0],radius=1.5,
                    colors=[color(0.9), color(0.15)],
                    startangle = 90,
                    counterclock = False)
  plt.setp( outer_ring, width=ring_width, edgecolor=outer_edge_color)

  inner_ring, _ = ax.pie(ring_arrays[1],
                         radius=inner_radius,
                         colors=[color(0.55), color(0.05)],
                         startangle = 90,
                         counterclock = False)
  plt.setp(inner_ring, width=ring_width, edgecolor=inner_edge_color)

    # add labels and format plots
  add_center_label(df)
  add_current_label(df)
  add_sub_center_label(df)
  ax.axis('equal')
  plt.margins(0,0)
  plt.autoscale('enable')

  return plt

# call the chart maker function and display the chart
df = {'col1': [0, 0.20]}
plt.savefig(create_radial_chart(df, color_theme='Purple'))
plt.show()

# plt.savefig(create_radial_chart((df, color_theme='Purple'))
# Currently supported color themes: Grey, Purple, Blue, Green, Orange, Red