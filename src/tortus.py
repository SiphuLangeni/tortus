import pandas as pd
from datetime import datetime
import ipywidgets as widgets
from ipywidgets import HTML, Output, Layout
from IPython.display import display, clear_output, SVG

# tortus_logo = SVG(data='../docs/_static/tortus_logo.svg')
# welcome = widgets.HTML("<h2 style='text-align:center'>easy text annotation in a Jupyter Notebook</h2>")
# display(tortus_logo, welcome)

class Tortus:
    '''Text annotation within a Jupyter Notebook
    
    :attr annotation_index: A counter for the annotations in progress.

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

    :param labels: Annotation labels., default=['Positive', 'Negative', 'Neutral']
    :type labels: list
    '''
    
    annotation_index = 0

    def __init__(self, df, text, num_records=10, id_column=None, annotations=None, random=True,
                labels=['Positve', 'Negative', 'Neutral']):
        '''Initializes the Tortus class.'''
        
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
        self.labels = labels
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

        with open('../docs/_build/html/_images/tortus_logo.png', 'rb') as image_file:
            image = image_file.read()
            logo = widgets.Image(value=image, format='png', width='40%')

        rules = widgets.HTML(
            '<h4>Click on the label corresponding with the text below. Each selection requires \
                confirmation before proceeding to the next item.</h4>')
        annotation_text = self.subset_df.iloc[self.annotation_index, -1]
        text = widgets.HTML(self.subset_df.iloc[self.annotation_index, -1])
        
        labels = []
        for label in self.labels:
            label_button = widgets.Button(description=label,
                                          layout=Layout(border='solid'))
            label_button.style.button_color = '#eeeeee'
            label_button.style.font_weight = 'bold'
            labels.append(label_button)

        label_buttons = widgets.HBox(labels)
        skip_button = widgets.Button(description='Skip',
                                     layout=Layout(border='solid'))
        skip_button.style.button_color = '#eeeeee'
        skip_button.style.font_weight = 'bold'
        confirm_button = widgets.Button(description='Confirm selection',
                                        layout=Layout(border='solid'))
        confirm_button.style.button_color = '#eeeeee'
        confirm_button.style.font_weight = 'bold'
        redo_button = widgets.Button(description='Try again',
                                     layout=Layout(border='solid'))
        redo_button.style.button_color = '#eeeeee'
        redo_button.style.font_weight = 'bold'
        progress_bar = widgets.IntProgress(
                value=self.annotation_index,
                min=0,
                max=self.num_records,
                step=1,
                description=f'{self.annotation_index + 1}/{self.num_records}',
                bar_style='',
                orientation='horizontal',
                layout=Layout(width='50%', align_content='center'))
        progress_bar.style.bar_color = '#36a849'
    
        
        header = widgets.VBox([widgets.HBox([logo, progress_bar]), rules])
        sentiment_buttons = widgets.HBox([label_buttons, skip_button])
        confirmation_buttons = widgets.HBox([confirm_button, redo_button])
        output = widgets.Output()

        display(header, text, sentiment_buttons, confirmation_buttons, output)
        confirmation_buttons.layout.visibility = 'hidden'    


        def label_buttons_clicked(button):
            '''Response to button click of any sentiment buttons.
            
            Appends ``annotations`` with label selection.
            :param button: Label buttons click. 
            '''
            button.style.button_color = '#36a849'
            record_id = self.create_record_id()
            self.annotations.loc[len(self.annotations)] = [
                record_id[self.annotation_index],
                self.subset_df[self.text].iloc[self.annotation_index],
                str(button.description).lower(),
                datetime.now().replace(microsecond=0)  
            ]
            
            for label in labels:
                label.disabled = True
                if button != label:
                    label.layout.border = 'None'

            skip_button.disabled = True
            skip_button.layout.border = 'None'
                
            with output:
                clear_output(True)
                sentiment_buttons.layout.visibility = 'visible'
                confirmation_buttons.layout.visibility = 'visible'

        for label in labels:
            label.on_click(label_buttons_clicked)
            # label.visibility
            # label.style.button_color = '#36a849'

        def skip_button_clicked(button):
            '''Response to button click of the skip button.

            Appends ``annotations``. Label value is ``Null``.
            
            :param button: Skip button click.
            '''
            button.style.button_color = '#36a849'
            record_id = self.create_record_id()
            self.annotations.loc[len(self.annotations)] = [
                record_id[self.annotation_index],
                self.subset_df[self.text].iloc[self.annotation_index],
                None,
                datetime.now().replace(microsecond=0)  
            ]
            for label in labels:
                label.disabled = True
                label.layout.border = 'None'

            skip_button.disabled = True
                
            with output:
                clear_output(True)
                sentiment_buttons.layout.visibility = 'visible'
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
                    orientation='horizontal',
                    layout=Layout(width='75%', align_content='center'))
                progress_bar.style.bar_color = '#36a849'
                display(HTML("<h3 style='text-align:center'>Annotations are complete.</h3>"))
                display (progress_bar)

        confirm_button.on_click(confirm_button_clicked)

        def redo_button_clicked(button):
            '''Response to click of the redo button.

            Deletes the most recent input to ``annotations``.
            
            :param button: Redo button click.
            '''
            self.annotations.drop([self.annotation_index], inplace=True)
            for label in labels:
                label.style.button_color = '#eeeeee'
                label.disabled = False
                label.layout.border = 'solid'
                
            skip_button.style.button_color = '#eeeeee'
            skip_button.disabled = False
            skip_button.layout.border = 'solid'

            with output:
                clear_output(True)
                sentiment_buttons.layout.visibility = 'visible'
                confirmation_buttons.layout.visibility = 'hidden'


        redo_button.on_click(redo_button_clicked)

