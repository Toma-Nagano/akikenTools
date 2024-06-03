import os
import warnings
import numpy as np
import pandas as pd
import cv2


def custom_warning_formatter(message, category, filename, lineno, file=None, line=None) -> str:
    return f"{category.__name__}: {message}\n"


def img_processing(path: str, trim_range: tuple, size: tuple) -> np.ndarray:
    '''
    Args:
        path (str): 画像ファイルのパス
        trim_range (tuple): 画像をクリッピングする範囲 (Left x, Right x, Upper y, Lower y)
        size (tuple): 画像のリサイズ後のサイズ (Width, Height)

    Returns:
        img (numpy.ndarray): 前処理を実施した画像データ

    Raises:
        FileNotFoundError: The specified path does not exist.
            指定されたパスが存在しない場合
        ValueError: The specified path does not point to a file.
            指定されたパスがファイルを指していない場合
        ValueError: The specified path does not point to an image file.
            指定されたパスが画像ファイルでない場合
        ValueError: Input tuple size is wrong. 
            入力されたタプルのサイズが異なる場合
    '''
    if len(trim_range) != 4 or len(size) != 2:
        raise ValueError('Input tuple size is wrong.')
    if not os.path.exists(path):
        raise FileNotFoundError('The specified path does not exist.')
    if not os.path.isfile(path):
        raise ValueError('The specified path does not point to a file.')
    if not path.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
        raise ValueError('The specified path does not point to an image file.')
    else:
        img = cv2.imread(path)
        img = img[trim_range[2]:trim_range[3], trim_range[0]:trim_range[1], :]
        img = cv2.resize(img, dsize=size)
    return img


def make_folder(path: str, target: str, name: str, trim_range: tuple, size: tuple) -> None:
    '''
    Args:
        path (str): オリジナル画像ディレクトリのパス
        target (str): 前処理後の画像ディレクトリを作成する場所のパス
        name (str): 作成する画像ディレクトリの名前
        trim_range (tuple): 画像をクリッピングする範囲 (Left x, Right x, Upper y, Lower y)
        size (tuple): 画像のリサイズ後のサイズ (Width, Height)

    Returns:
        None: ディレクトリを自動作成し、画像をアップロードする

    Raises:
        FileNotFoundError: The specified path does not exist.
            指定されたパスが存在しない場合
        ValueError: The specified path does not point to a directory.
            指定されたパスがディレクトリを指していない場合
        FileExistsError: The directory already exists.
            作成するディレクトリが既に存在する場合
        ValueError: The number of files exceeds 1000.
            オリジナル画像が1000を超える場合

    Note:
        画像ファイルの名前は 'img' に連番を付けたものになります

        この命名法では、1000枚目以降の画像は命名できません
    '''
    if not os.path.exists(path) or not os.path.exists(target):
        raise FileNotFoundError('The specified path does not exist.')
    if not os.path.isdir(path) or not os.path.isdir(target):
        raise ValueError('The specified path does not point to a directory.')
    folder = os.path.join(target, name)
    if os.path.exists(folder):
        raise FileExistsError('The directory already exists.')
    else:
        os.mkdir(folder)
        count = 0
        for file in sorted(os.listdir(path)):
            if file.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                count += 1
                file = os.path.join(path, file)
                img = img_processing(file, trim_range, size)
                if count < 10:
                    cv2.imwrite(os.path.join(folder, f'img00{count}.png'), img)
                elif count < 100:
                    cv2.imwrite(os.path.join(folder, f'img0{count}.png'), img)
                elif count < 1000:
                    cv2.imwrite(os.path.join(folder, f'img{count}.png'), img)
                else:
                    raise ValueError('The number of files exceeds 1000.')
        print(f'{count} images have been uploaded.')
    return


def make_average_img(path: str) -> np.ndarray:
    '''
    Args:
        path (str): 画像ディレクトリのパス

    Returns:
        img (numpy.ndarray): 平均画像データ

    Raises:
        FileNotFoundError: The specified path does not exist.
            指定されたパスが存在しない場合
        ValueError: The specified path does not point to a directory.
            指定されたパスがディレクトリを指していない場合
        FileNotFoundError: No image file exists at the specified path.
            指定されたパスに画像ファイルが存在しない場合

    Warning:
        [ number ] images are not used because of different sizes.
            画像サイズが異なるため、平均画像の作成に使用されなかった画像の数を表示
    '''
    if not os.path.exists(path):
        raise FileNotFoundError('The specified path does not exist.')
    if not os.path.isdir(path):
        raise ValueError('The specified path does not point to a directory.')
    else:
        imagesNum = 0
        imagesWarn = 0
        warnList = []
        for file in sorted(os.listdir(path)):
            if file.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                source = os.path.join(path, file)
                img = cv2.imread(source)
                if imagesNum == 0:
                    ave_img = np.zeros(img.shape)
                if img.shape == ave_img.shape:
                    ave_img += img
                    imagesNum += 1
                else:
                    imagesWarn += 1
                    warnList.append(file)
        if imagesNum == 0:
            raise FileNotFoundError(
                'No image file exists at the specified path.')
        else:
            ave_img = ave_img / imagesNum
            ave_img = ave_img.astype(np.uint8)
        if imagesWarn > 0:
            text = f'{imagesWarn} images are not used because of different sizes.\n' + \
                str(warnList)
            warnings.formatwarning = custom_warning_formatter
            warnings.warn(text)
    return ave_img


def calc_MSE(target: str | np.ndarray, source: str | np.ndarray, option: bool = False) -> float | tuple[float, np.ndarray]:
    '''
    Args:
        target (str | numpy.ndarray): MSEを算出したい画像ファイルのパスまたは数値データ
        source (str | numpy.ndarray): 平均画像ファイルのパスまたは数値データ
        option (bool = False): True を指定すると差分画像を返す

    Returns:
        mse_value (float): 平均二乗誤差の計算結果
        diff_img (numpy.ndarray , optional): 差分画像の数値データ

    Raises:
        TypeError: The type for the specified argument is incorrect.
            指定された引数のデータ型が正しくない場合
        ValueError: The input image sizes do not match.
            入力画像のサイズが一致しない場合
    '''
    if not isinstance(target, (str, np.ndarray)) or not isinstance(source, (str, np.ndarray)):
        raise TypeError('The type for the specified argument is incorrect.')
    if isinstance(target, str):
        target = cv2.imread(target)
    if isinstance(source, str):
        source = cv2.imread(source)
    if target.shape != source.shape:
        raise ValueError('The input image sizes do not match.')
    else:
        diff_img = target - source
        mse_value = np.mean(diff_img ** 2)
    if option:
        return mse_value, diff_img
    else:
        return mse_value


def calc_RMSE_table(path: str, source: str | np.ndarray) -> pd.DataFrame:
    '''
    Args:
        path (str): 画像ディレクトリのパス
        source (str | numpy.ndarray): 平均画像ファイルのパスまたは数値データ

    Returns:
        RMSE_table (pandas.DataFrame): 画像ファイル名、MSE、RMSE の表

    Raises:
        FileNotFoundError: The specified path does not exist.
            指定されたパスが存在しない場合
        ValueError: The specified path does not point to a directory.
            指定されたパスがディレクトリを指していない場合
    '''
    if not os.path.exists(path):
        raise FileNotFoundError('The specified path does not exist.')
    if not os.path.isdir(path):
        raise ValueError('The specified path does not point to a directory.')
    else:
        if isinstance(source, str):
            source = cv2.imread(source)
        image_list = []
        mse_list = []
        rmse_list = []
        for file in sorted(os.listdir(path)):
            if file.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                image_list.append(file)
                target = os.path.join(path, file)
                mse_value = calc_MSE(target, source)
                rmse_value = np.sqrt(mse_value)
                mse_list.append(mse_value)
                rmse_list.append(rmse_value)
        RMSE_table = pd.DataFrame(
            {'FileName': image_list, 'MSE': mse_list, 'RMSE': rmse_list})
    return RMSE_table


def get_RGB(img: str | np.ndarray, y: int, convert: bool = True) -> pd.DataFrame:
    '''
    Args:
        img (str | numpy.ndarray): 画像ファイルのパスまたは数値データ
        y (int): 取得する行の y 座標
        convert (bool = True): BGR 型式から RGB 型式に変換するかどうか

    Returns:
        RGB_table (pandas.DataFrame): 特定行の RGB 値の表

    Raises:
        ValueError: The specified data is not in the proper format.
            指定されたデータが適切な形式でない場合
        ValueError: The specified y coordinate is out of range.
            指定された y 座標が範囲外の場合
    '''
    if isinstance(img, str):
        img = cv2.imread(img)
    if img.ndim != 3 or img.shape[2] != 3:
        raise ValueError('The specified data is not in the proper format.')
    if y < 0 or y >= img.shape[0]:
        raise ValueError('The specified y coordinate is out of range.')
    else:
        if convert:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        RGB_table = pd.DataFrame(img[y, :, :], columns=['R', 'G', 'B'])
        RGB_table.insert(0, 'X', range(len(RGB_table)))
    return RGB_table
