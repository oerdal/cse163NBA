import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc
import seaborn as sns

# credit to http://savvastjortjoglou.com/nba-shot-sharts.html for
# the below utility function, which draws a basketball court using
# patches in matplotlib
# we can draw a set of matplotlib shapes on the above plot, to be able to build a more powerful data visualization
def make_court(ax=None, color='black', lw=2, outer_lines=False):
    if ax is None:
        ax = plt.gca()
    elem = []
    rim = Circle((0,0), radius=7.5, linewidth=lw, color=color, fill=False)
    elem.append(rim)
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw,
                               color=color)
    elem.append(corner_three_a)
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    elem.append(corner_three_b)
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw,
                    color=color)
    elem.append(three_arc)
    backboard = Rectangle((-30, -7.5), 60, -1, linewidth=lw, color=color)

    # The paint
    # Create the outer box 0f the paint, width=16ft, height=19ft
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color,
                          fill=False)
    # Create the inner box of the paint, widt=12ft, height=19ft
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color,
                          fill=False)

    # Create free throw top arc
    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180,
                         linewidth=lw, color=color, fill=False)
    # Create free throw bottom arc
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0,
                            linewidth=lw, color=color, linestyle='dashed')
    # Restricted Zone, it is an arc with 4ft radius from center of the hoop
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw,
                     color=color)
    center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0,
                           linewidth=lw, color=color)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0,
                           linewidth=lw, color=color)
    back_bound = Rectangle((-250,-47.5), 500, 0, color=color, linewidth=lw)
    left_bound = Rectangle((-250,-47.5), 0, 470, color=color, linewidth=lw)
    right_bound = Rectangle((250,-47.5), 0, 470, color=color, linewidth=lw)
    center_court = Rectangle((-250, 422.5), 500, 0, color=color, linewidth=lw)
    elem.append(center_inner_arc)
    elem.append(center_outer_arc)
    elem.append(backboard)
    elem.append(outer_box)
    elem.append(inner_box)
    elem.append(top_free_throw)
    elem.append(bottom_free_throw)
    elem.append(restricted)
    elem.append(back_bound)
    elem.append(left_bound)
    elem.append(right_bound)
    elem.append(center_court)
    for e in elem:
        ax.add_patch(e)
    return ax

# additional utility function added to utilize above function, plots the
# shot data for a given player (optionally, but always supplied),
# and optionally a given year
def make_shot_chart(shots, name=None, ax=None, year=None):
    if name is not None:
        data = shots[(shots['PLAYER_NAME'] == name)]
    else:
        data = shots
    if year is not None:
        data = data[data['YEAR'] == year]
    plt.figure(num=None, figsize=(11, 11), dpi=80, facecolor='w', edgecolor='k')
    ax = plt.gca() if ax is None else ax
    make_court(ax=ax, outer_lines=True)
    sns.scatterplot(x="LOC_X", y="LOC_Y", data=data, hue='SHOT_MADE_FLAG', ax=ax)
    plt.xlim(-300,300)
    plt.ylim(-100,500)
    plt.xlabel("")
    plt.ylabel("")
    plt.title("Shot chart: {}".format(name))
    plt.show()
    plt.savefig("./shot_charts/{}_{}.png".format(name, year))