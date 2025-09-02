# Importa o arquivo que eu escrevi o código
import medical_data_visualizer
from unittest import main

# Testa as funções
medical_data_visualizer.draw_cat_plot()
medical_data_visualizer.draw_heat_map()

#Roda os testes
main(module='test_module', exit=False)