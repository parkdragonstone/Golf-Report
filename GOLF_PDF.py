from fpdf import FPDF
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams['figure.facecolor'] = (0.168, 0.188, 0.239)
plt.rcParams['axes.facecolor'] = (0.168, 0.188, 0.239)
plt.rcParams['text.color'] = 'white'
plt.rcParams['axes.labelcolor'] = 'white'
plt.rcParams['xtick.color'] = 'white'
plt.rcParams['ytick.color'] = 'white'
plt.rcParams['xtick.labelsize'] = 16
plt.rcParams['ytick.labelsize'] = 16
plt.rcParams['axes.titlesize'] = 20  # 축 제목의 기본 폰트 크기를 20으로 설정
plt.rcParams['axes.labelsize'] = 19
plt.rcParams['axes.edgecolor'] = 'white'
plt.rcParams['figure.figsize'] = 14, 6
plt.rcParams['legend.fontsize'] = 16

class PDF(FPDF):
    def create_table(self, table_data, title='', data_size = 10, title_size=12, align_data='L', align_header='L', cell_width='even', x_start='x_default',emphasize_data=[], emphasize_style=None,emphasize_color=(0,0,0)): 
        """
        table_data: 
                    list of lists with first element being list of headers
        title: 
                    (Optional) title of table (optional)
        data_size: 
                    the font size of table data
        title_size: 
                    the font size fo the title of the table
        align_data: 
                    align table data
                    L = left align
                    C = center align
                    R = right align
        align_header: 
                    align table data
                    L = left align
                    C = center align
                    R = right align
        cell_width: 
                    even: evenly distribute cell/column width
                    uneven: base cell size on lenght of cell/column items
                    int: int value for width of each cell/column
                    list of ints: list equal to number of columns with the widht of each cell / column
        x_start: 
                    where the left edge of table should start
                    'C' - center
        emphasize_data:  
                    which data elements are to be emphasized - pass as list 
                    emphasize_style: the font style you want emphaized data to take
                    emphasize_color: emphasize color (if other than black) 
        
        """
        default_style = self.font_style
        if emphasize_style == None:
            emphasize_style = default_style
        # default_font = self.font_family
        # default_size = self.font_size_pt
        # default_style = self.font_style
        # default_color = self.color # This does not work

        # Get Width of Columns
        def get_col_widths():
            col_width = cell_width
            if col_width == 'even':
                col_width = self.epw / len(data[0]) - 1  # distribute content evenly   # epw = effective page width (width of page not including margins)
            elif col_width == 'uneven':
                col_widths = []

                # searching through columns for largest sized cell (not rows but cols)
                for col in range(len(table_data[0])): # for every row
                    longest = 0 
                    for row in range(len(table_data)):
                        cell_value = str(table_data[row][col])
                        value_length = self.get_string_width(cell_value)
                        if value_length > longest:
                            longest = value_length
                    col_widths.append(longest + 4) # add 4 for padding
                col_width = col_widths



                        ### compare columns 

            elif isinstance(cell_width, list):
                col_width = cell_width  # TODO: convert all items in list to int        
            else:
                # TODO: Add try catch
                col_width = int(col_width)
            return col_width

        # Convert dict to lol
        # Why? because i built it with lol first and added dict func after
        # Is there performance differences?
        if isinstance(table_data, dict):
            header = [key for key in table_data]
            data = []
            for key in table_data:
                value = table_data[key]
                data.append(value)
            # need to zip so data is in correct format (first, second, third --> not first, first, first)
            data = [list(a) for a in zip(*data)]

        else:
            header = table_data[0]
            data = table_data[1:]

        line_height = self.font_size * 2.5

        col_width = get_col_widths()
        self.set_font(family='Arial', style='B', size=title_size)

        # Get starting position of x
        # Determin width of table to get x starting point for centred table
        if x_start == 'C':
            table_width = 0
            if isinstance(col_width, list):
                for width in col_width:
                    table_width += width
            else: # need to multiply cell width by number of cells to get table width 
                table_width = col_width * len(table_data[0])
            # Get x start by subtracting table width from pdf width and divide by 2 (margins)
            margin_width = self.w - table_width
            # TODO: Check if table_width is larger than pdf width

            center_table = margin_width / 2 # only want width of left margin not both
            x_start = center_table
            self.set_x(x_start)
        elif isinstance(x_start, int):
            self.set_x(x_start)
        elif x_start == 'x_default':
            x_start = self.set_x(self.l_margin)


        # TABLE CREATION #

        # add title
        if title != '':
            self.multi_cell(0, line_height, title, border=0, align='j', ln=3, max_line_height=self.font_size)
            self.ln(line_height)  # Move the cursor down by 3 units after multi_cell

        self.set_font(size=data_size)
        # add header
        y1 = self.get_y()
        if x_start:
            x_left = x_start
        else:
            x_left = self.get_x()
        x_right = self.epw + x_left
        if  not isinstance(col_width, list):
            if x_start:
                self.set_x(x_start)
            for datum in header:
                self.multi_cell(col_width, line_height, datum, border=0, align=align_header, ln=3, max_line_height=self.font_size)
                x_right = self.get_x()
            self.ln(line_height) # move cursor back to the left margin
            y2 = self.get_y()
            self.set_draw_color(255, 255, 255)  
            self.line(x_left,y1,x_right,y1)
            self.line(x_left,y2,x_right,y2)

            for row in data:
                if x_start: # not sure if I need this
                    self.set_x(x_start)
                for datum in row:
                    if datum in emphasize_data:
                        self.set_text_color(*emphasize_color)
                        self.set_font(style=emphasize_style)
                        self.multi_cell(col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=self.font_size)
                        self.set_text_color(0,0,0)
                        self.set_font(style=default_style)
                    else:
                        self.multi_cell(col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=self.font_size) # ln = 3 - move cursor to right with same vertical offset # this uses an object named self
                self.ln(line_height) # move cursor back to the left margin
        
        else:
            if x_start:
                self.set_x(x_start)
            for i in range(len(header)):
                datum = header[i]
                self.multi_cell(col_width[i], line_height, datum, border=0, align=align_header, ln=3, max_line_height=self.font_size)
                x_right = self.get_x()
            self.ln(line_height) # move cursor back to the left margin
            y2 = self.get_y()
            self.set_draw_color(255, 255, 255)  
            self.line(x_left,y1,x_right,y1)
            self.line(x_left,y2,x_right,y2)


            for i in range(len(data)):
                if x_start:
                    self.set_x(x_start)
                row = data[i]
                for i in range(len(row)):
                    datum = row[i]
                    if not isinstance(datum, str):
                        datum = str(datum)
                    adjusted_col_width = col_width[i]
                    if datum in emphasize_data:
                        self.set_text_color(*emphasize_color)
                        self.set_font(style=emphasize_style)
                        self.multi_cell(adjusted_col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=self.font_size)
                        self.set_text_color(0,0,0)
                        self.set_font(style=default_style)
                    else:
                        self.multi_cell(adjusted_col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=self.font_size) # ln = 3 - move cursor to right with same vertical offset # this uses an object named self
                self.ln(line_height) # move cursor back to the left margin
        y3 = self.get_y()
        self.set_draw_color(255, 255, 255)  
        self.line(x_left,y3,x_right,y3)
        



class UPLIFT_REPORT_GRAPH_DATA():
    def kinematic_sequence(data, ks_cols, time, address, top,impact):
        ks = {
            'peak' : {},
            'time' : {},
            }
        fig, ax = plt.subplots()

        for col in ks_cols:
            plt.plot(time, data[col], color = ks_cols[col][-1], label=ks_cols[col][0], lw=3)
            
            ks['peak'][col] = round(data[col][:impact+60].max(), 2)
            ks['time'][col] = np.where(data[col] == data[col][:impact+60].max())[0][0]        
            plt.axvline(time[ks['time'][col]],lw=3,color = ks_cols[col][-1], linestyle ='--', alpha= 0.7)
                
        plt.ylabel('Angular Velocity [deg/s]')
        plt.xlabel('Time [s]')
        plt.autoscale(axis='x', tight=True)
        plt.axvline(time[address], color='white',linestyle = '--',alpha=0.5, lw=5)
        plt.axvline(time[top], color='white',linestyle = '--',alpha=0.5, lw=5)
        plt.axvline(time[impact], color='white',linestyle = '--',alpha=0.5, lw=5)

        plt.axhline(0,color='white',lw=0.9)
        
        plt.text(time[address+1] ,y = data['left_arm_rotational_velocity_with_respect_to_ground'].max(), s='ADD' ,rotation = 90, verticalalignment='top',horizontalalignment='left', fontsize=16)
        plt.text(time[top+1],y = data['left_arm_rotational_velocity_with_respect_to_ground'].max(), s='BST',rotation = 90, verticalalignment='top',horizontalalignment='left', fontsize=16)
        plt.text(time[impact+1] ,y = data['left_arm_rotational_velocity_with_respect_to_ground'].max(), s='IMP' ,rotation = 90, verticalalignment='top',horizontalalignment='left', fontsize=16)
        plt.legend(loc=3)
        plt.tight_layout()

        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.grid(axis='y')
        plt.savefig(f"Figure/kinematic.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        return ks
    
    def one_angle(data, cols, time, address, top, impact):
        ang = {
            'max' : {},
            'max_frame' : {},
            'min' : {},
            'min_frame' : {},
            'address' : {},
            'top' : {},
            'impact': {},
            }
        
        for col in cols:
            
            df = data[col]
            
            fig, ax = plt.subplots()
            plt.plot(time, df, color = 'firebrick', lw=3)

            ang['address'][col]   = round(df[address], 2)
            ang['top'][col]   = round(df[top], 2)
            ang['impact'][col]  = round(df[impact], 2)
            
            ang['max'][col]       = round(df.max(), 2)
            ang['max_frame'][col] = np.where(df == df.max())[0][0]
            ang['min'][col]       = round(df.min(), 2)
            ang['min_frame'][col] = np.where(df == df.min())[0][0]
        
            if col in ['trunk_twist_clockwise']: # 최솟값
                plt.axvline(time[np.where(df == df.min())[0][0]], color = 'firebrick', lw=3, linestyle = '--',alpha=0.7)
            
            if col in ['head_twist_clockwise',
                       'left_elbow_flexion','right_elbow_flexion',]: # 최댓값
                plt.axvline(time[np.where(df == df.max())[0][0]], color = 'firebrick', lw=3, linestyle = '--',alpha=0.7)
            
            if col in ['left_knee_extension']:
                ang['min'][col]       = round(df.iloc[top:impact+1].min(), 2)
                ang['min_frame'][col] = np.where(df == df.iloc[top:impact+1].min())[0][0]
                plt.axvline(time[np.where(df == df.iloc[top:impact+1].min())[0][0]], color = 'firebrick', lw=3, linestyle = '--',alpha=0.7)
            
            if col in ['head_lateral_flexion_clockwise','right_knee_extension','trunk_lateral_flexion_right']:
                ang['max'][col]       = round(df.iloc[top:impact+1].max(), 2)
                ang['max_frame'][col] = np.where(df == df.iloc[top:impact+1].max())[0][0]
                plt.axvline(time[np.where(df == df.iloc[top:impact+1].max())[0][0]], color = 'firebrick', lw=3, linestyle = '--',alpha=0.7) 
            
            if col in ['right_shoulder_adduction','right_shoulder_horizontal_adduction']:
                ang['min'][col]       = round(df.iloc[:impact+1].min(), 2)
                ang['min_frame'][col] = np.where(df == df.iloc[:impact+1].min())[0][0]
                plt.axvline(time[np.where(df == df.iloc[:impact+1].min())[0][0]], color = 'firebrick', lw=3, linestyle = '--',alpha=0.7)
            
            if col in ['left_shoulder_adduction','left_shoulder_horizontal_adduction']:
                ang['max'][col]       = round(df.iloc[:impact+1].max(), 2)
                ang['max_frame'][col] = np.where(df == df.iloc[:impact+1].max())[0][0]
                plt.axvline(time[np.where(df == df.iloc[:impact+1].max())[0][0]], color = 'firebrick', lw=3, linestyle = '--',alpha=0.7)
            
            m = df.max()    
            
            plt.ylabel(f'Angle [deg]')
            plt.xlabel('Time [s]')
            plt.autoscale(axis='x', tight=True)
            plt.axvline(time[address]  ,color='white' ,linestyle = '--' ,alpha=0.5, lw=5)
            plt.axvline(time[top]  ,color='white' ,linestyle = '--' ,alpha=0.5, lw=5)
            plt.axvline(time[impact] ,color='white' ,linestyle = '--' ,alpha=0.5, lw=5)

            plt.axhline(0,color='white',lw=0.9)
            
            plt.text(time[address+1], y = m, s='ADD',rotation = 90, verticalalignment='top',horizontalalignment='left', fontsize=16)
            plt.text(time[top+1], y = m, s='BST',rotation = 90, verticalalignment='top',horizontalalignment='left', fontsize=16)
            plt.text(time[impact+1], y = m, s='IMP', rotation = 90, verticalalignment='top',horizontalalignment='left', fontsize=16)
            
            plt.tight_layout()

            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.grid(axis='y')
            plt.savefig(f"Figure/{cols[col]}.png", dpi=300, bbox_inches='tight')
            plt.close()
        
        return ang
    

    def one_vel(data, cols, time, address, top, impact):
        vel = {
            'max' : {},
            'max_frame' : {},
            'min' : {},
            'min_frame' : {},
            'address' : {},
            'top' : {},
            'impact': {},
            }
        
        for col in cols:
            
            df = data[col]
            
            fig, ax = plt.subplots()
            plt.plot(time, df, color = 'firebrick', lw=3)

            vel['address'][col]   = round(df[address], 2)
            vel['top'][col]   = round(df[top], 2)
            vel['impact'][col]  = round(df[impact], 2)
            
            vel['max'][col]       = round(df.max(), 2)
            vel['max_frame'][col] = np.where(df == df.max())[0][0]
            vel['min'][col]       = round(df.min(), 2)
            vel['min_frame'][col] = np.where(df == df.min())[0][0]
        
            if col in ['right_elbow_flexion_velocity']: # 최솟값
                plt.axvline(time[np.where(df == df.min())[0][0]], color = 'firebrick', linestyle = '--',alpha=0.7, lw=3)
            
            if col in ['trunk_lateral_flexion_right']: # 최댓값
                plt.axvline(time[np.where(df == df.max())[0][0]], color = 'firebrick', linestyle = '--',alpha=0.7, lw=3)
            
            if col in ['left_elbow_flexion_velocity']:
                vel['min'][col]       = round(df.iloc[top:impact+1].min(), 2)
                vel['min_frame'][col] = np.where(df == df.iloc[top:impact+1].min())[0][0]
                plt.axvline(time[np.where(df == df.iloc[top:impact+1].min())[0][0]], color = 'firebrick', linestyle = '--',alpha=0.7, lw=3)
                
            if col in ['left_knee_extension_velocity','trunk_twist_clockwise_velocity','right_knee_extension_velocity']:
                vel['max'][col]       = round(df.iloc[top:impact+1].max(), 2)
                vel['max_frame'][col] = np.where(df == df.iloc[top:impact+1].max())[0][0]
                plt.axvline(time[np.where(df == df.iloc[top:impact+1].max())[0][0]], color = 'firebrick', linestyle = '--',alpha=0.7, lw=3)    
            m = df.max()    
            
            plt.ylabel('Angular Velcocity [deg/s]')
            plt.xlabel('Time [s]')
            plt.autoscale(axis='x', tight=True)
            plt.axvline(time[address]  ,color='white' ,linestyle = '--' ,alpha=0.5, lw=5)
            plt.axvline(time[top]  ,color='white' ,linestyle = '--' ,alpha=0.5, lw=5)
            plt.axvline(time[impact] ,color='white',linestyle = '--' ,alpha=0.5, lw=5)

            plt.axhline(0,color='white',lw=0.9)
            
            plt.text(time[address+1], y = m, s='ADD',rotation = 90, verticalalignment='top',horizontalalignment='left', fontsize=16)
            plt.text(time[top+1], y = m, s='BST',rotation = 90, verticalalignment='top',horizontalalignment='left', fontsize=16)
            plt.text(time[impact+1], y = m, s='IMP', rotation = 90, verticalalignment='top',horizontalalignment='left', fontsize=16)
            
            plt.tight_layout()

            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.grid(axis='y')
            plt.savefig(f"Figure/{cols[col]}.png", dpi=300, bbox_inches='tight')
            plt.close()
        
        return vel
    
    def displacement(data, ks_cols, time, address, top,impact):
        dis = {
            'address' : {},
            'top' : {},
            'impact': {},
            }
        
        fig, ax = plt.subplots()
        for col in ks_cols:
            df = (data[col] - data[col][0]) * 100
            if col in ['pelvis_3d_z','proximal_neck_3d_z']:
                df = - df
            plt.plot(time, df, color = ks_cols[col][-1], label=ks_cols[col][0], lw=3)
            dis['address'][col]   = round(df[address], 1)
            dis['top'][col]   = round(df[top], 1)
            dis['impact'][col]  = round(df[impact], 1)
                
        plt.ylabel('Displacement [cm]')
        plt.xlabel('Time [s]')
        plt.autoscale(axis='x', tight=True)
        plt.axvline(time[address], color='white',linestyle = '--',alpha=0.5, lw=5)
        plt.axvline(time[top], color='white',linestyle = '--',alpha=0.5, lw=5)
        plt.axvline(time[impact], color='white',linestyle = '--',alpha=0.5, lw=5)

        plt.axhline(0,color='white',lw=0.9)
        
        plt.text(time[address+1] ,y = df.max(), s='ADD' ,rotation = 90, verticalalignment='top',horizontalalignment='left', fontsize=16)
        plt.text(time[top+1],y = df.max(), s='BST',rotation = 90, verticalalignment='top',horizontalalignment='left', fontsize=16)
        plt.text(time[impact+1] ,y =df.max(), s='IMP' ,rotation = 90, verticalalignment='top',horizontalalignment='left', fontsize=16)
        plt.legend(loc=3)
        plt.tight_layout()

        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.grid(axis='y')
        plt.savefig(f"Figure/{col}_displacement.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        return dis
    
    def pelvis_trunk_angle(data, ks_cols, time, address, top,impact):
        dis = {
            'address' : {},
            'top' : {},
            'impact': {},
            }
        
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        
        for col in ks_cols:
            df = data[col]
            if ks_cols[col][0] == 'Lateral Tilt':
                color = ks_cols[col][-1]
                ax2.plot(time, df, color = ks_cols[col][-1], label=ks_cols[col][0], lw=3)
                ax2.set_ylabel('Lateral Tilt Angle[°]', color = color)
                ax2.tick_params(axis='y', labelcolor=color)
            
            else:
                ax1.plot(time, df, color=ks_cols[col][-1], label=ks_cols[col][0], lw=3)
                color = ks_cols[col][-1]
            dis['address'][col]   = round(df[address], 1)
            dis['top'][col]   = round(df[top], 1)
            dis['impact'][col]  = round(df[impact], 1)
                    
        ax1.set_ylabel('Rotation Angle [°]',color = color)
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.set_xlabel('Time [s]')
        ax1.autoscale(axis='x', tight=True)
        ax1.axvline(time[address], color='white', linestyle='--', alpha=0.5, lw=5)
        ax1.axvline(time[top], color='white', linestyle='--', alpha=0.5, lw=5)
        ax1.axvline(time[impact], color='white', linestyle='--', alpha=0.5, lw=5)
        ax1.axhline(0, color='white', lw=0.9)
        
        # 여기서 df.max() 대신 적절한 값으로 변경할 필요가 있습니다.
        ax1.text(time[address+1], y=ax1.get_ylim()[1], s='ADD', rotation=90, verticalalignment='top', horizontalalignment='left', fontsize=16)
        ax1.text(time[top+1], y=ax1.get_ylim()[1], s='BST', rotation=90, verticalalignment='top', horizontalalignment='left', fontsize=16)
        ax1.text(time[impact+1], y=ax1.get_ylim()[1], s='IMP', rotation=90, verticalalignment='top', horizontalalignment='left', fontsize=16)
        
        ax1.legend(loc=3)
        ax2.legend(loc=4)  # 두 번째 y축 범례 위치 설정
        
        plt.tight_layout()

        ax1.spines['right'].set_visible(False)
        ax1.spines['top'].set_visible(False)
        ax1.spines['bottom'].set_visible(False)
        ax1.grid(axis='y')

        plt.savefig(f"Figure/{col}_angle.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        return dis