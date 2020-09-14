import pandas as pd
from datetime import datetime
import ipywidgets as widgets
from ipywidgets import HTML, Output
from IPython.display import display, clear_output

class Tortus:
    '''Text annotation within a Jupyter Notebook
    
    :attr annotation_index: A counter for the annotations in progress.
    '''
    
    annotation_index = 0

    def __init__(self, df, text, num_records=10, id_column=None, annotations=None, random=True):
        '''Initializes the Tortus class.
       
        :param df: A dataframe with texts that need to be annotated.
        :type df: pandas.core.frame.DataFrame

        :param text: The name of the column containing the text to be annotated.
        :type text: str

        :param num_records: (default=10) Number of records to annotate.
        :type num_records: int
        
        :param id_column: (default=None) The name of the column containing ID of the text.
            If None, ``id_column`` will correspond to the index of ``df``.
        :type id_column: str

        :param annotations: (default=None) The dataframe with annotations previously created in this tool.
            If None, ``annotations`` is created with columns ``id_column``, ``text``, ``label``, ``annotated_at``.
        :type annotation_df: pandas.core.frame.DataFrame

        :param random: (default=True) Determines if records are loaded randomly or sequentially.
        :type random: bool
        '''
        
        self.df = df
        self.text = text
        self.num_records = num_records
        self.id_column = id_column
        if annotations is None:
            if id_column is None:
                self.annotations = pd.DataFrame(columns=['id_column', text, 'label', 'annotated_at'])
            else:
                self.annotations = pd.DataFrame(columns=[id_column, text,'label','annotated_at'])
        else:
            self.annotations = annotations.copy()
        self.random = random
        self.subset_df = self.create_subset_df()
           
    def create_subset_df(self):
        '''
        Subsets ``df`` to include only records cued for annotation.

        If ``annotations`` already exists, those records will excuded from the annotation tool.

        :returns: A dataframe that will be used in the annotation tool.
        :rtype: pandas.core.frame.DataFrame
        '''

        if self.annotations.empty:
            subset_df = self.df.copy()

        else:
            leave_out = self.annotations[self.text].to_list()
            subset_df = self.df[~self.df[self.text].isin(leave_out)]

        if self.random:
            try:
                subset_df = subset_df.sample(n=self.num_records)[[self.id_column, self.text]]
            except:
                subset_df = subset_df.sample(n=self.num_records)[[self.text]]
        else:
            try:
                subset_df = subset_df[[self.id_column, self.text]][:self.num_records]
            except:
                subset_df = subset_df[[self.text]][:self.num_records]

        return subset_df

    def create_record_id(self):
        '''Provides a record id for ``annotations``.

        :returns: A list of record ids that refer to each text in subset df created by 
            :meth:`create_subset_df` method.
        :rtype: list
        '''

        if self.id_column is None:
            record_id = self.subset_df.index.to_list()
        else:
            record_id = self.subset_df[self.id_column].to_list()
        return record_id
        
    def annotate(self):
        '''Displays texts to be annotated in a UI. Loads user inputted labels and timestamps into
            ``annotations`` dataframe.
        '''
        with open('Images/tortus250.png', 'rb') as image_file:
            image = image_file.read()
        logo = widgets.Image(value=image, format='png')
        instructions = widgets.HTML(
            '<b>Click on the appropriate sentiment for the text below. Each selection requires \
                confirmation before proceeding to the next item. To retrieve your annotations \
                at any time, call <i>your_instance.annotations</i></b>.')
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
        sentiment_buttons = widgets.HBox([positive_button, negative_button, neutral_button, skip_button, quit_button])
        confirmation_buttons = widgets.HBox([confirm_button, redo_button])
        output = widgets.Output()

        display(logo_box, instructions, text, sentiment_buttons, confirmation_buttons, progress_bar, output)
        confirmation_buttons.layout.visibility = 'hidden'    


        def sentiment_button_clicked(button):
            '''Response to button click of any sentiment buttons.
            
            Appends ``annotations`` with label selection.
            :param button: Sentiment button click. 
            '''
            record_id = self.create_record_id()
            self.annotations.loc[len(self.annotations)] = [
                record_id[self.annotation_index],
                self.subset_df[self.text].iloc[self.annotation_index],
                str(button.description).lower(),
                datetime.now().replace(microsecond=0)  
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
            '''Response to button click of the skip button.

            Appends ``annotations``. Label value is ``Null``.
            
            :param button: Skip button click.
            '''
            record_id = self.create_record_id()
            self.annotations.loc[len(self.annotations)] = [
                record_id[self.annotation_index],
                self.subset_df[self.text].iloc[self.annotation_index],
                None,
                datetime.now().replace(microsecond=0)  
            ]
            
            with output:
                clear_output(True)
                sentiment_buttons.layout.visibility = 'hidden'
                print('This action will add a Null value to the label for this record.')
                confirmation_buttons.layout.visibility = 'visible'

        skip_button.on_click(skip_button_clicked)

        def confirm_button_clicked(button):
            '''Response to click of the confirm button.

            Advances the ``annotation_index`` to view the next item in the annotation tool.
                Indicates the tool is done if ``annotation_index`` does not advance further.
            
            :param button: Confirmation button click.
            '''
            if self.annotation_index < len(self.subset_df) - 1:
                self.annotation_index += 1
                clear_output(True)
                self.annotate()
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
            '''Response to click of the redo button.

            Deletes the most recent input to ``annotations``.
            
            :param button: Redo button click.
            '''
            self.annotations.drop([self.annotation_index], inplace=True)
        
            with output:
                clear_output(True)
                sentiment_buttons.layout.visibility = 'visible'
                print('Please try again.')
                confirmation_buttons.layout.visibility = 'hidden'


        redo_button.on_click(redo_button_clicked)

        def quit_button_clicked(button):
            '''Response to click of the quit button.

            Stops the annotation tool and shows a progress bar to indicate how many texts were annotated.
            
            :param button: Quit button click.
            '''
            clear_output(True)
            progress_bar = widgets.IntProgress(
                value=self.annotation_index,
                min=0,
                max=self.num_records,
                step=1,
                description=f'{self.annotation_index}/{self.num_records}',
                bar_style='',
                orientation='horizontal')
            display(HTML('<h3>Annotations stopped.</h3>'))
            display (progress_bar)
            
        quit_button.on_click(quit_button_clicked)
