import os
import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
import pandas as pd
from menu import Clusterer  # Import the Clusterer class from your module

# Redirect standard output and error to nothing
sys.stdout = open(os.devnull, 'w')
sys.stderr = open(os.devnull, 'w')

class ClusteringApp(App):
    ''' Build the Kivy application interface. '''
    def build(self):
        self.file_path = ""
        self.num_clusters = 0

        # Layout
        layout = BoxLayout(orientation='vertical', padding=10)

        # FileChooser
        self.file_chooser = FileChooserListView()
        self.file_chooser.filters = ["*.csv"]
        self.file_chooser.bind(on_submit=self.selected)
        layout.add_widget(Label(text="Select CSV File:"))
        layout.add_widget(self.file_chooser)

        # Input for number of clusters
        self.num_clusters_input = TextInput(hint_text="Enter number of clusters", multiline=False)
        layout.add_widget(Label(text="Number of Clusters:"))
        layout.add_widget(self.num_clusters_input)

        # Button to start clustering
        start_button = Button(text="Start Clustering", size_hint=(None, None), size=(150, 50))
        start_button.bind(on_press=self.start_clustering)
        layout.add_widget(start_button)

        return layout

    ''' Callback function when a file is selected using the FileChooser. '''
    def selected(self, filechooser, file_path, *args):
        self.file_path = file_path[0] if file_path else ""

    ''' Callback function to start the clustering process. '''
    def start_clustering(self, instance):
        try:
            self.num_clusters = int(self.num_clusters_input.text)
            if self.num_clusters <= 0:
                raise ValueError("Number of clusters must be a positive integer.")
        except ValueError as e:
            self.show_error_popup("Invalid Input", str(e))
            return

        if not self.file_path:
            self.show_error_popup("Error", "Please select a CSV file.")
            return

        # Check file size
        file_size_kb = os.path.getsize(self.file_path) / 1024
        if file_size_kb > 70:
            self.show_error_popup("Error", "File size exceeds the limit (70KB). Please select a smaller file.")
            return

        # Perform clustering
        if self.file_path:
            try:
                data = pd.read_csv(self.file_path, na_values='?', encoding='utf-8')
            except Exception as e:
                self.show_error_popup("Error", f"Error loading CSV file: {str(e)}")
                return

            clusterer = Clusterer(self.num_clusters, len(data.columns))
            clustering_result = clusterer.cluster(data)

            # Display clustering results
            self.show_clustered_popup(data, clustering_result, self.num_clusters, 1)

    ''' Display clustering results in a popup window. '''
    def show_clustered_popup(self, data, clustering, num_clusters, decimals):
        popup = Popup(title="Clustering Results", size_hint=(0.9, 0.9))

        clusters_layout = GridLayout(cols=3, spacing=10, size_hint_y=None)
        clusters_layout.bind(minimum_height=clusters_layout.setter('height'))

        clusters = {}

        for i, row in enumerate(data.values):
            cluster_id = clustering[i]
            if cluster_id not in clusters:
                clusters[cluster_id] = []
            clusters[cluster_id].append(row)

        for k, rows in clusters.items():
            cluster_label = Label(text=f"Cluster {k}:", font_size=16, bold=True)
            clusters_layout.add_widget(cluster_label)

            cluster_content = GridLayout(cols=1, spacing=5, size_hint_y=None)
            cluster_content.bind(minimum_height=cluster_content.setter('height'))

            for row in rows:
                row_text = " ".join([f"{value:.{decimals}f}" if isinstance(value, (int, float)) else str(value) for value in row])
                row_label = Label(text=row_text)
                cluster_content.add_widget(row_label)

            clusters_layout.add_widget(cluster_content)

        scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        scroll_view.add_widget(clusters_layout)

        popup.add_widget(scroll_view)
        popup.open()

    ''' Display error messages in a popup window. '''
    def show_error_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

if __name__ == '__main__':
    ClusteringApp().run()

    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__