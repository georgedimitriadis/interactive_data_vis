


import threading
import dearpygui.dearpygui as dpg
import numpy as np


def _kill_dpg_thread():
    global plot_thread
    plot_thread = False
    dpg.stop_dearpygui()


def _generate_data(data_var_names, data_gen_function_name):
    global _globals_
    data_x = None

    if data_var_names is not None:
        if type(data_var_names) == tuple or type(data_var_names) == list or type(data_var_names) == np.ndarray:
            if len(data_var_names) == 2:
                data_x = _globals_[data_var_names[0]]
                data_y = _globals_[data_var_names[1]]
            elif len(data_var_names) == 1:
                data_y = _globals_[data_var_names[0]]
        elif type(data_var_names) == str:
            data_y = _globals_[data_var_names]
    else:
        result_data = _globals_[data_gen_function_name]()
        if type(result_data) == tuple:
            data_x, data_y = result_data
        else:
            data_y = result_data

    return data_x, data_y


def _start_plot_thread(data_var_names=None, data_gen_function_name=None):
    print(1)
    data_x, data_y = _generate_data(data_var_names, data_gen_function_name)
    print(2)
    dpg.create_context()
    print(3)
    dpg.create_viewport(title='Plotting Window', width=900, height=400, decorated=True)
    print(4)
    dpg.setup_dearpygui()
    print(5)
    with dpg.window(label="Graph", width=900, height=400, show=True, tag='graph') as plot_id:
        with dpg.group(horizontal=True, tag='plot_group', parent='graph'):
            print(6)
            with dpg.plot(label="Line plot", width=800, height=400, tag='line_plot', parent='plot_group'):
                print(7)
                dpg.add_plot_axis(dpg.mvXAxis, label="x", tag='x_axis', parent='line_plot')
                dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis", parent='line_plot')

                dpg.add_line_series(data_x, data_y, parent="y_axis", tag='line')
                print(8)
            dpg.add_button(label='X', callback=_kill_dpg_thread, width=-20, height=25, tag='X_plot_button',
                           parent='plot_group')
            print(9)
    dpg.show_viewport()
    print(10)
    #dpg.set_primary_window(plot_id, True)
    while dpg.is_dearpygui_running():
        if data_var_names is None:
            data_x, data_y = _generate_data(data_var_names, data_gen_function_name)
            dpg.set_value('line', [data_x, data_y])
        dpg.render_dearpygui_frame()
    dpg.destroy_context()


def plot(_globals, data_var_names=None, data_gen_function=None):
    global _globals_
    _globals_ = _globals

    assert (data_var_names is not None or data_gen_function is not None) and \
            not (data_var_names is not None and data_gen_function is not None), \
            'EITHER pass the name of the variable holding the data to be plotted OR ' \
            'the function that will generate them'

    data_gen_function_name = None
    if data_gen_function is not None:
        data_gen_function_name = data_gen_function.__name__

    plot_thread = threading.Thread(group=None, target=_start_plot_thread, args=(data_var_names, data_gen_function_name),
                                   daemon=True)
    plot_thread.start()