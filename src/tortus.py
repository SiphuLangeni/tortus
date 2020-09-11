import pandas as pd
from datetime import datetime
import ipywidgets as widgets
from ipywidgets import HTML, Output
from IPython.display import display, clear_output

class Tortus:
    
    annotation_index = 0

    def __init__(self, df, id_column, text, annotation_df=None, num_records=10, random=True):
        
        self.df = df
        self.id_column = id_column
        self.text = text
        if annotation_df is None:
            self.annotations = pd.DataFrame(columns=[id_column, text,'label','annotated_at'])
        else:
            self.annotations = annotation_df.copy()
        self.num_records = num_records
        self.random = random
        self.subset_df = self.create_subset_df()
            
    def create_subset_df(self):
        '''
        Subsets the dataframe by the primary key and text columns with a chosen number of records.
        '''
        if self.annotations.empty:
            subset_df = self.df.copy()

        else:
            leave_out = self.annotations[self.text].to_list()
            subset_df = self.df[~self.df[self.text].isin(leave_out)]

        if self.random:
            subset_df = subset_df.sample(n=self.num_records)[[self.id_column, self.text]]
        else:
            subset_df = subset_df[[self.id_column, self.text]][:self.num_records]

        return subset_df
        
        
    def load_annotations(self):
        '''
        Displays texts to be annotated and loads user inputted labels and timestamp to dataframe.
        '''
        with open('Images/tortus250.png', 'rb') as image_file:
            image = image_file.read()
        logo = widgets.Image(value=image, format='png')
        instructions = widgets.HTML("<b>Click on the appropriate sentiment for the text below:</b>")
        text = HTML(self.subset_df.iloc[self.annotation_index, 1])
        positive_button = widgets.Button(description='Positive')
        negative_button = widgets.Button(description='Negative')
        neutral_button = widgets.Button(description='Neutral')
        skip_button = widgets.Button(description='Skip')
        confirm_button = widgets.Button(description='Confirm selection')
        redo_button = widgets.Button(description='Try again')
        quit_button = widgets.Button(description='Quit')
        progress_bar = widgets.IntProgress(
                value=self.annotation_index,
                min=0,
                max=self.num_records,
                step=1,
                description=f'{self.annotation_index + 1}/{self.num_records}',
                bar_style='',
                orientation='horizontal')
        
        logo_layout = widgets.Layout(
                display='flex',
                flex_flow='column',
                align_items='center',
                width='100%')
        logo_box = widgets.HBox(children=[logo],layout=logo_layout)
        
        sentiment_buttons = widgets.HBox([positive_button, negative_button, neutral_button, skip_button])
        confirmation_buttons = widgets.HBox([confirm_button, redo_button, quit_button])
        output = widgets.Output()

        display(logo_box, instructions, text, sentiment_buttons, widgets.HBox([confirmation_buttons, progress_bar]), output)
        confirmation_buttons.layout.visibility = 'hidden'    


        def sentiment_button_clicked(button):
            self.annotations.loc[len(self.annotations)] = [
                self.subset_df[self.id_column].iloc[self.annotation_index],
                self.subset_df[self.text].iloc[self.annotation_index],
                str(button.description).lower(),
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
            ]

            with output:
                clear_output(True)
                sentiment_buttons.layout.visibility = 'hidden'
                print('The text has', str(button.description).lower(), 'sentiment.')
                confirmation_buttons.layout.visibility = 'visible'

        positive_button.on_click(sentiment_button_clicked)
        negative_button.on_click(sentiment_button_clicked)
        neutral_button.on_click(sentiment_button_clicked)

        def skip_button_clicked(button):
            self.annotations.loc[len(self.annotations)] = [
                self.subset_df[self.id_column].iloc[self.annotation_index],
                self.subset_df[self.text].iloc[self.annotation_index],
                None,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
            ]
            
            with output:
                clear_output(True)
                sentiment_buttons.layout.visibility = 'hidden'
                print('This action will add a Null value to the label for this record.')
                confirmation_buttons.layout.visibility = 'visible'

        skip_button.on_click(skip_button_clicked)

        def confirm_button_clicked(button):
            if self.annotation_index < len(self.subset_df) - 1:
                self.annotation_index += 1
                clear_output(True)
                self.load_annotations()
            else:

                clear_output(True)
                progress_bar = widgets.IntProgress(
                    value=self.num_records,
                    min=0,
                    max=self.num_records,
                    step=1,
                    description=f'{self.annotation_index + 1}/{self.num_records}',
                    bar_style='',
                    orientation='horizontal')
                display(HTML('<h3>Annotations are complete.</h3>'))
                display (progress_bar)

        confirm_button.on_click(confirm_button_clicked)

        def redo_button_clicked(button):
            self.annotations.drop([self.annotation_index], inplace=True)
        
            with output:
                clear_output(True)
                sentiment_buttons.layout.visibility = 'visible'
                print('Please try again.')
                confirmation_buttons.layout.visibility = 'hidden'


        redo_button.on_click(redo_button_clicked)

        def quit_button_clicked(button):
            clear_output(True)
            progress_bar = widgets.IntProgress(
                value=self.annotation_index + 1,
                min=0,
                max=self.num_records,
                step=1,
                description=f'{self.annotation_index + 1}/{self.num_records}',
                bar_style='',
                orientation='horizontal')
            display(HTML('<h3>Annotations stopped.</h3>'))
            display (progress_bar)
            
        quit_button.on_click(quit_button_clicked)

    def annotate(self):
        self.load_annotations()
