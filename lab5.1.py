# Лабараторна робота №5
# Візуалізація даних
# Невмержицька Дар'я ФБ-23
# Мета роботи: отримати поглиблені навички з візуалізації даних; ознайомитись з matplotlib.widgets, scipy.signal.filters, а також з Plotly, Bokeh, Altair; отримати навички зі створення інтерактивних застосунків для швидкого підбору параметрів і аналізу отриманих результатів
# Хід роботи:


#Імпортуємо бібліотеки
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
from scipy.signal import butter, filtfilt

# Ініціалізація змінної для зберігання попереднього шумового сигналу
previous_noise_signal = None

# Оновлення параметрів при зміні віджетів
def update(val):
    global previous_noise_signal
    
    # Перевірка типу події від віджета
    if isinstance(val, str):  # Подія з чекбокса
        update_noise = False
        update_visibility(val)
        #update_noise = True if val == 'Show Noise' else False
    else:  # Подія з слайдера
        if val in [noise_mean_slider.val, noise_cov_slider.val]:
            update_noise = True
        else:
            update_noise = True if previous_noise_signal is None else False
    
    # Отримання значень параметрів з віджетів
    amplitude = amp_slider.val
    frequency = freq_slider.val
    phase = phase_slider.val
    noise_mean = noise_mean_slider.val
    noise_covariance = noise_cov_slider.val
    filter_cutoff = filter_cutoff_slider.val
    filter_fs = filter_fs_slider.val

    # Отримання стану чекбоксів
    add_noise = check_show_noise.get_status()[0]
    filters_noise = check_filters_noise.get_status()[0]
    
    # Виклик функції генерації гармонічного сигналу з шумом
    harmonic_with_noise(amplitude, frequency, phase, noise_mean, noise_covariance, add_noise=add_noise, update_noise=update_noise, filters_noise=filters_noise, cutoff=filter_cutoff, fs=filter_fs)

# Скидання всіх параметрів до значень за замовчуванням
def reset(event):
    global previous_noise_signal
    previous_noise_signal = None

    # Скидання значень слайдерів
    amp_slider.reset()
    freq_slider.reset()
    phase_slider.reset()
    noise_mean_slider.reset()
    noise_cov_slider.reset()
    filter_cutoff_slider.reset()
    filter_fs_slider.reset()

    # Скидання стану чекбоксів
    check_show_noise.set_active(True)
    check_filters_noise.set_active(True)
    
    # Оновлення графіку
    update(None)

# Фільтрація сигналу (фільтр Баттерворта)
def filter_signal(signal_to_filter, cutoff, fs):
    # Визначення частоти Нюквіста
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    # Отримання коефіцієнтів фільтру Баттерворта
    b, a = butter(2, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, signal_to_filter)
    return y

# Генерація гармонічного сигналу
def harmonic_with_noise(amplitude, frequency, phase, noise_mean, noise_covariance, add_noise=True, update_noise=True, filters_noise=True, cutoff=0.5, fs=30):
    global previous_noise_signal
    t = np.linspace(0, 5, 1000)
    harmonic_signal = amplitude * np.sin(frequency * t + phase)
    
    # Генерація шуму та додавання його до сигналу, якщо вибрано опцію показу шуму
    if add_noise:  
        if previous_noise_signal is None or update_noise:
            noise = np.random.multivariate_normal([0, 0], [[noise_covariance, 0], [0, noise_covariance]], len(t))
            noise_signal = noise[:, 0] + noise_mean
            previous_noise_signal = noise_signal
        else:
            noise_signal = previous_noise_signal
        signal = harmonic_signal + noise_signal

        # Фільтрація сигналу, якщо вибрано опцію фільтрації
        if filters_noise:
            filtered_signal = filter_signal(signal, cutoff, fs)
    else:
        signal = harmonic_signal

    # Очищення графіку та побудова нового сигналу
    ax.clear()
    ax.plot(t, signal, label='Signal')
    if add_noise and filters_noise:
        ax.plot(t, filtered_signal, label='Filtered Signal')
    ax.set_xlabel('Time')
    ax.set_ylabel('Amplitude')
    ax.legend()
    plt.draw()

# Показ або приховування слайдерів фільтру залежно від стану чекбокса "Show Filter"
def update_visibility(label):
    if label == 'Show Noise':
        if check_show_noise.get_status()[0]:
            noise_mean_slider_ax.set_visible(True)
            noise_cov_slider_ax.set_visible(True)
        else:
            noise_mean_slider_ax.set_visible(False)
            noise_cov_slider_ax.set_visible(False)
    if label == 'Filters Noise':
        if check_filters_noise.get_status()[0]:
            filter_cutoff_slider_ax.set_visible(True)
            filter_fs_slider_ax.set_visible(True)
        else:
            filter_cutoff_slider_ax.set_visible(False)
            filter_fs_slider_ax.set_visible(False)
    plt.draw()

# Створення графіку
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.4)
harmonic_with_noise(1, 3, 0, 0, 0.01)

# Створення віджетів слайдерів та кнопок
amp_slider_ax = plt.axes([0.15, 0.28, 0.57, 0.03])
amp_slider = Slider(amp_slider_ax, 'Amplitude', 0.1, 5.0, valinit=1)
amp_slider.on_changed(update)

freq_slider_ax = plt.axes([0.15, 0.24, 0.57, 0.03])
freq_slider = Slider(freq_slider_ax, 'Frequency', 0.1, 10.0, valinit=3)
freq_slider.on_changed(update)

phase_slider_ax = plt.axes([0.15, 0.20, 0.57, 0.03])
phase_slider = Slider(phase_slider_ax, 'Phase', 0, 2*np.pi, valinit=0)
phase_slider.on_changed(update)

noise_mean_slider_ax = plt.axes([0.15, 0.16, 0.57, 0.03])
noise_mean_slider = Slider(noise_mean_slider_ax, 'Noise Mean', -1, 1, valinit=0)
noise_mean_slider.on_changed(update)

noise_cov_slider_ax = plt.axes([0.15, 0.12, 0.57, 0.03])
noise_cov_slider = Slider(noise_cov_slider_ax, 'Noise Covariance', 0, 0.2, valinit=0.01)
noise_cov_slider.on_changed(update)

filter_cutoff_slider_ax = plt.axes([0.15, 0.08, 0.57, 0.03])
filter_cutoff_slider = Slider(filter_cutoff_slider_ax, 'Filter (cutoff)', 0, 5.0, valinit=0.5)
filter_cutoff_slider.on_changed(update)

filter_fs_slider_ax = plt.axes([0.15, 0.04, 0.57, 0.03])
filter_fs_slider = Slider(filter_fs_slider_ax, 'Filter (fs)', 0, 100.0, valinit=30)
filter_fs_slider.on_changed(update)

# Створення віджетів чекбоксів
check_show_noise_ax = plt.axes([0.8, 0.25, 0.1, 0.15])
check_show_noise = CheckButtons(check_show_noise_ax, ['Show Noise'], [True])
check_show_noise.on_clicked(update)

check_filters_noise_ax = plt.axes([0.8, 0.15, 0.1, 0.15])
check_filters_noise = CheckButtons(check_filters_noise_ax, ['Filters Noise'], [True])
check_filters_noise.on_clicked(update)

# Створення кнопки скидання
reset_ax = plt.axes([0.8, 0.15, 0.1, 0.05])
reset_button = Button(reset_ax, 'Reset')
reset_button.on_clicked(reset)

# Показ графіку
plt.show()
