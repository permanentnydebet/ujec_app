
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


class DataProcessor:
    def __init__(self):
        pass

    def process_file(self, csv_file_path):
         # - read file
        self.df = pd.read_csv(csv_file_path)

        # Fill missing values with the last non-zero value in each column
        self.df.ffill(inplace=True)

        # Convert the 'time' column to a datetime object for time-based operations
        self.df['time'] = pd.to_datetime(self.df['time'], format="%H:%M:%S.%f")

        # Set 'time' as the index for the DataFrame
        self.df.set_index('time', inplace=True)

        # Read start and stop times from the CSV file (assuming they are in the 'time' column)
        self.default_start_time = self.df.index.min()
        self.default_stop_time = self.df.index.max()
        self.default_resample_value = '1S'
        self.is_resample = False

        self.start_time = self.default_start_time
        self.stop_time =  self.default_stop_time
        self.resample_value = self.default_resample_value

        self.number_of_rows = self.df.shape[0]

    def get_measuement_name(self):
        return self.df.columns.tolist()

    def change_resample(self, resample_value):
        if resample_value < 0:
            return False

        if resample_value == 0:
            self.is_resample = False
        else:
            self.resample_value = resample_value
            self.is_resample = True

        return True

    def plot(self, list_of_column):
        df_show = self.df
        if self.is_resample is True:
            df_show = self.df.resample(str(self.resample_value) + 's').mean()

        df_show = df_show.loc[self.start_time:self.stop_time]
        df_show.reset_index(inplace=True)

        # Create a scatter plot for 'Age' and 'OtherColumn'
        fig = go.Figure()

        for column in list_of_column:
            fig.add_trace(go.Scatter(x=df_show['time'], y=df_show[column], name=column))


        fig.update_layout(title='Multiple Columns Plot',
                  xaxis_title='Name',
                  yaxis_title='Values',
                  hovermode='x unified',  # Display the vertical line on hover
                  hoverdistance=5)  #

        # fig = px.line(df_show, x='time', y=column_to_plot, labels={column_to_plot: column_to_plot})
        fig.show()

    def get_time(self):
        return self.default_start_time, self.default_stop_time


    def change_start_time(self, start_time):
        start_time = pd.to_datetime(start_time)

        if start_time < self.default_start_time or start_time > self.stop_time:
            return False

        self.start_time = start_time
        return True

    def change_stop_time(self, stop_time):
        stop_time= pd.to_datetime(stop_time)
        if stop_time > self.default_stop_time or stop_time < self.start_time:
            return False

        self.stop_time = stop_time
        return True
