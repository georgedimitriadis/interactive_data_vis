

import threading
import dearpygui.dearpygui as dpg


def _slider_callback(sender, app_data, user_data):
    _globals_[user_data] = dpg.get_value(sender)


def _kill_dpg_thread():
    dpg.stop_dearpygui()


def _start_slider_thread(slider_var_name, min_max_values=None):
    global _globals_
    
    slider_var_name = slider_var_name[0]
    slider_type = type(_globals_[slider_var_name])
    assert slider_type == int or slider_type == float, \
        'The type of the tracked variable must be either an in or a float'

    dpg.create_context()
    dpg.create_viewport(title='Slider Window', width=800, height=40, decorated=False)
    dpg.setup_dearpygui()

    with dpg.window(label="Slider", width=800, height=40, show=True, tag='slider_win') as slider_id:
        with dpg.group(horizontal=True, parent='slider_win', tag='slider_group'):
            dpg.add_text(default_value='{} = '.format(slider_var_name), parent='slider_group')
            dpg.add_spacer(width=10, parent='slider_group')
            if slider_type == int:
                if min_max_values is not None:
                    slider = dpg.add_slider_int(callback=_slider_callback, user_data=slider_var_name, width=-60,
                                                default_value=_globals_[slider_var_name], tag='slider',
                                                min_value=min_max_values[0], max_value=min_max_values[1],
                                                parent='slider_group')
                else:
                    slider = dpg.add_slider_int(callback=_slider_callback, user_data=slider_var_name, width=-60,
                                                default_value=_globals_[slider_var_name], tag='slider',
                                                parent='slider_group')
            if slider_type == float:
                if min_max_values is not None:
                    slider = dpg.add_slider_float(callback=_slider_callback, user_data=slider_var_name, width=-60,
                                                  default_value=_globals_[slider_var_name], tag='slider',
                                                  min_value=min_max_values[0], max_value=min_max_values[1],
                                                  parent='slider_group')
                else:
                    slider = dpg.add_slider_float(callback=_slider_callback, user_data=slider_var_name, width=-60,
                                                  default_value=_globals_[slider_var_name], tag='slider',
                                                  parent='slider_group')
            dpg.add_button(label='X', callback=_kill_dpg_thread, width=-20, height=25, tag='X_slider_button',
                           parent='slider_group')

    dpg.show_viewport()
    dpg.set_primary_window(slider_id, True)
    while dpg.is_dearpygui_running():
        dpg.set_value(slider, _globals_[slider_var_name])
        dpg.render_dearpygui_frame()
    dpg.destroy_context()


def slider(_globals, tracker_var, min_max_values=None):
    global _globals_
    _globals_ = _globals
    
    tracker_var_name = [i for i, j in _globals_.items() if j == tracker_var]
    assert len(tracker_var_name) == 1, 'There is more than one variables with value = {}. ' \
                                       'Give the variable you are passing a unique value'.format(tracker_var)
    slider_thread = threading.Thread(group=None, target=_start_slider_thread, args=(tracker_var_name, min_max_values),
                                     daemon=True)
    slider_thread.start()
