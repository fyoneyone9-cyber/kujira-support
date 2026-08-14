for path in [
    r'C:\Users\fyone\Desktop\my-support\src\app\(app)\dashboard\page.tsx',
    r'C:\Users\fyone\Desktop\kujira-support\src\app\(app)\dashboard\page.tsx',
]:
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    # Slack（くじら）= TB82LHSPM、Slack（個人）= T07G6EHESKG に修正
    # 現状: くじらラベルにT07G6EHESKG、個人ラベルにTB82LHSPM → URLを入れ替え
    c = c.replace('T07G6EHESKG/C07GD3LRMD0', '__KOJIN__')
    c = c.replace('TB82LHSPM/CB82LJ1B5', 'T07G6EHESKG/C07GD3LRMD0')
    c = c.replace('__KOJIN__', 'TB82LHSPM/CB82LJ1B5')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print('done:', path)
