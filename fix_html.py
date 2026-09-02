from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEME_STYLESHEET = 'readable-theme.css'
THEME_SCRIPT = 'readable-theme.js'
BRAIN_TRAINING_SCRIPT = 'brain-training.js'

GENERATED_MARKERS = (
    "EXPERIENCE_STYLES",
    "EXPERIENCE_MARKUP",
    "EXPERIENCE_SCRIPT",
    "SPEECH_CONTROLS",
    "TEXT_SIZE_CONTROLS",
)

explanations = {
    'akarusa.html': '画面が見にくいときや文字が小さすぎるときに使います。スマートフォンの右上から下に指を滑らせてコントロールパネルを開きます。太陽の印がある明るさのスライダーを上に動かすと画面が明るくなり、下に動かすと暗くなります。目が疲れない明るさに調整してください。ほかのアプリからもこの設定にもどってくるので、一度調整すれば毎回簡単に明るさを変えられます。',
    'wifi.html': 'インターネットに接続するために使います。スマートフォンの設定を開いて、ワイファイのところをタップします。ご家庭のワイファイを選んで、パスワードを入力してください。接続できると、画面の上に電波のようなマークが表示されます。ワイファイに接続すると、ラインやメール、ウェブサイト閲覧が快適にできるようになります。',
    'oto.html': '音の大きさを調整して、電話の着信を聞き取りやすくします。スマートフォンの右側にある音量ボタンで調整できます。上のボタンで音が大きくなり、下のボタンで音が小さくなります。音量設定の画面で、各アプリごとに音量を変えることもできます。難聴の方は、特に電話と着信音の音量を大きめに設定することをお勧めします。',
    'juudenn.html': 'スマートフォンのバッテリーがなくなるのを防ぎます。付属のケーブルをスマートフォンに接続して、コンセントに差し込みます。緑色のライトが点灯したら充電開始です。画面で充電の進み具合が確認できます。バッテリーが100パーセントになったら充電完了です。毎日使うスマートフォンは、毎晩充電するのがお勧めです。',
    'kihonn.html': 'スマートフォン全体の基本的な設定を変更できます。設定アプリを開いて、各項目から必要な設定を選択します。言語、日付、時刻、位置情報など、さまざまな設定が集約されています。最初の設定時に一度調整しておくと、その後の操作が快適になります。',
    'line.html': 'ラインはメッセージアプリで、知人とのやり取りに使います。インスタグラムは写真や動画を共有するアプリです。どちらもダウンロードしたら、まずアカウントを作成してください。登録後は、相手を検索して友達追加すれば、やり取りが始められます。無料でメッセージ送受信ができるので、通話料をかけずに連絡が取れます。',
    'dennwa.html': '相手に電話をかけたり、電話を受けたりします。電話アプリを開いて、電話番号を入力して撥号ボタンを押すと、通話が開始されます。着信があると、画面に着信者の名前や番号が表示されます。電話を受けるときは、緑色の応答ボタンをタップします。電話を切るときは赤いボタンをタップします。',
    'nizigenn.html': '二次元コード（QRコード）を使って、ウェブサイトや情報に素早くアクセスできます。カメラアプリを立ち上げて、二次元コードに向かわせます。コードが認識されると、画面に通知が現れます。その通知をタップすると、関連するウェブサイトや情報が開きます。チラシや看板の二次元コードを読み取ることで、簡単に詳しい情報にアクセスできます。',
    'map.html': 'どこかに行きたいとき、道順を調べるのに使います。マップアプリを開いて、目的地の名前や住所を入力します。現在地から目的地までの道順と、所要時間が表示されます。徒歩、電車、車など、移動手段を選択することもできます。矢印の方向に進めば、目的地にたどり着けます。',
    'densya.html': '電車で移動するとき、乗り換える駅や時間を調べるのに使います。移動の案内アプリを開いて、出発地と目的地を入力します。そうすると、電車の行き先、乗る方向、降りる駅が表示されます。運行遅延の情報もリアルタイムで更新されるので、最新の情報が確認できます。',
    'karendar.html': 'カレンダーは予定を記録するのに使い、アラームは時間を知らせるのに使います。カレンダーアプリで日付をタップして、その日の予定を入力します。アラームアプリで時間を設定すると、その時刻になると音声で通知されます。毎日の予定や薬の時間を記録して、忘れないようにできます。',
    'hosuukei.html': '毎日何歩歩いたかを記録して、健康管理に役立てます。歩数計アプリは、スマートフォンが自動的に歩数をカウントします。一日の歩数目標を設定することで、運動習慣の改善に役立ちます。毎日の歩数の推移をグラフで確認することもできます。',
    'ap.html': 'アプリはスマートフォンのプログラムのことで、新しい機能を追加します。アプリストアを開いて、必要なアプリを検索して、ダウンロードボタンをタップします。ダウンロードが完了すると、スマートフォンのホーム画面にアプリが追加されます。不要なアプリは長押しして、削除することもできます。',
    'seiri.html': 'ホーム画面の使いやすさを改善します。アプリのアイコンを長押しして、別の位置にドラッグして移動できます。不要なアプリは削除することで、画面をスッキリさせられます。アプリをホルダーにまとめることで、探しやすくなります。',
    'syasinn.html': 'スマートフォンで写真を撮影します。カメラアプリを開いて、撮りたいものに向かわせます。シャッターボタンをタップすると、写真が撮影されます。撮影済みの写真は、写真アプリでいつでも確認して、家族や友人に送ることができます。',
    'koe.html': '話しかけるだけで、情報を検索することができます。マイクのアイコンをタップして、知りたいことを話しかけます。スマートフォンがあなたの声を認識して、検索結果を表示します。天気、時間、ニュースなど、さまざまな情報が音声で確認できます。',
    'kamera.html': 'カメラを虫眼鏡のように使って、小さい文字を大きく見ることができます。カメラアプリの虫眼鏡機能を有効にすると、ライトで照らしながら拡大表示できます。新聞や医療用の用紙など、小さい文字を読むときに便利です。',
    'ps.html': 'スマートフォンを安全に使うために、パスワードを管理します。各アプリやウェブサイトのパスワードを、安全に保存して管理できます。パスワード管理アプリを使うと、複雑なパスワードを覚える必要がなくなります。定期的にパスワードを変更することで、セキュリティが向上します。',
    'syoto.html': 'スマートフォンの画面そのものを写真に撮影します。スクリーンショットは、大切な情報を保存するのに便利です。通常、電源ボタンと音量を下げるボタンを同時に押すと、スクリーンショットが撮影されます。撮影されたスクリーンショットは、写真アプリに保存されます。',
    'saigai.html': '地震や大雨などの災害情報を素早く確認できます。災害情報アプリやウェブサイトにアクセスして、現在地の災害情報を確認します。緊急時は、全国の警報や注意報が表示されます。定期的に災害情報をチェックして、万が一に備えることができます。',
    'noutore.html': 'スマートフォンを使って、脳を活性化させるトレーニングができます。パズルやクイズなど、さまざまなゲームが用意されています。毎日少しの時間をかけてトレーニングすることで、認知機能の維持や向上に役立ちます。',
}

experience_steps = {
    'akarusa.html': ['画面の明るさを見直す', '右上から下へ指を動かす', '明るさスライダーを上に動かす', '見やすい明るさに合わせる', '設定が戻っても同じように調整する'],
    'wifi.html': ['設定アプリを開く', 'Wi‑Fiまたはネットワークを選ぶ', 'Wi‑Fiをオンにする', '接続先の一覧から家のネットワークを選ぶ', 'パスワードを確認して入力する', '接続できたら電波マークを確認する'],
    'oto.html': ['音量ボタンを見つける', '上のボタンで音を大きくする', '下のボタンで音を小さくする', '着信音の確認をする', 'アプリ別の音量にも気をつける'],
    'juudenn.html': ['ケーブルを確認する', 'スマホにケーブルを差し込む', 'コンセントに差し込む', '緑のランプを確認する', '充電の進み具合を画面で見る'],
    'kihonn.html': ['設定アプリを開く', '言語や日付を確認する', '必要な項目を選ぶ', '表示や通知を調整する', '自分に合う設定にまとめる'],
    'line.html': ['アプリを開く', '新規登録またはログインする', '友だちを探す', 'メッセージを送ってみる', '通話や写真の送信も試す'],
    'dennwa.html': ['電話アプリを開く', '連絡先または電話番号を選ぶ', '番号を入力する', '発信ボタンを押す', '応答や終了ボタンを確認する'],
    'nizigenn.html': ['カメラを開く', 'QRコードに向ける', 'コードが見える位置に調整する', '通知をタップする', '表示されたページを確認する'],
    'map.html': ['マップアプリを開く', '目的地を入力する', '出発地を確認する', '徒歩や電車を選ぶ', '経路と時間を見比べる'],
    'densya.html': ['案内アプリを開く', '出発地と目的地を入力する', '列車の路線を選ぶ', '乗り換えの回数を確認する', '時刻表と遅延情報を見て判断する'],
    'karendar.html': ['カレンダーを開く', '予定の日時を選ぶ', '予定の内容を入力する', 'アラームを設定する', '通知の時間を確認する'],
    'hosuukei.html': ['歩数計アプリを開く', '今日の数字を確認する', '目標を設定する', '歩いた記録を見直す', '習慣として続ける'],
    'ap.html': ['アプリストアを開く', '探したい機能を入れる', 'アプリを選ぶ', 'ダウンロードボタンを押す', 'ホーム画面で使う'],
    'seiri.html': ['アイコンを長押しする', '位置を動かす', '整理したいアプリを別の場所へ移す', '使わないアプリを消す', 'フォルダにまとめて見やすくする'],
    'syasinn.html': ['カメラを開く', '撮りたいものに向ける', 'シャッターを押す', '写真をプレビューする', '保存済みの写真を確認する'],
    'koe.html': ['マイクを押す', '質問をはっきり話す', '検索結果を確認する', '気になる言葉をもう一度聞く', '必要な情報を見つける'],
    'kamera.html': ['虫眼鏡機能をオンにする', '文字のある場所に近づける', 'ズームで大きくする', '文字の形を確認する', '見やすくなったら止める'],
    'ps.html': ['パスワード管理を開く', 'アカウントを選ぶ', '新しいパスワードを作る', '安全な保存場所を確認する', '定期的に見直す'],
    'syoto.html': ['画面を開いたまま確認する', '電源と音量小ボタンを同時に押す', '撮影した画像を確認する', '必要なら写真アプリで見直す', '保存場所を覚える'],
    'saigai.html': ['災害情報アプリを開く', '地域を確認する', '注意情報を読む', '避難ルートや連絡先を見ておく', '必要なときに見直す'],
    'noutore.html': ['脳トレアプリを開く', 'ゲームを選ぶ', 'まずは簡単な問題から始める', '少しずつ難しくする', '続けて習慣にする'],
}


def build_experience_markup(steps: list[str]) -> str:
    items = ''.join(
        f'<div class="experience-step" data-step="{index}">{index + 1}. {step}</div>'
        for index, step in enumerate(steps)
    )
    return f'''<!-- EXPERIENCE_MARKUP_START -->
    <div class="experience-panel" id="experience-panel" aria-labelledby="experience-title">
      <div class="experience-status" aria-live="polite">体験ステップ 1 / {len(steps)}</div>
      <h2 id="experience-title">体験してみよう</h2>
      <div class="experience-steps">{items}</div>
      <div class="button-row">
        <button type="button" class="action-btn" onclick="nextExperienceStep()">次のステップへ</button>
        <button type="button" class="action-btn stop-btn" onclick="resetExperience()">やり直す</button>
      </div>
    </div>
    <!-- EXPERIENCE_MARKUP_END -->'''


def _remove_marked_block(html_text: str, marker_name: str) -> str:
    pattern = rf'(?is)\s*<!--\s*{marker_name}_START\s*-->.*?<!--\s*{marker_name}_END\s*-->\s*'
    return re.sub(pattern, '\n', html_text)


def _find_balanced_div(html_text: str, start: int) -> tuple[int, int] | None:
    token_pattern = re.compile(r'</?div\b[^>]*>', re.IGNORECASE)
    depth = 0
    for match in token_pattern.finditer(html_text, start):
        if match.group(0).lower().startswith('</'):
            depth -= 1
        else:
            depth += 1
        if depth == 0:
            return start, match.end()
    return None


def _clean_legacy_experience_assets(html_text: str) -> str:
    legacy_style = re.compile(
        r'(?is)\s*<style>\s*\.experience-panel\s*\{.*?</style>\s*'
    )
    legacy_script = re.compile(
        r'''(?is)\s*<script>\s*\(function\s*\(\)\s*\{\s*'''
        r'''const\s+stepList\s*=\s*\[.*?'''
        r'''window\.addEventListener\(\s*['"]DOMContentLoaded['"]\s*,\s*renderExperience\s*\);\s*'''
        r'''\}\(\)\);\s*</script>\s*'''
    )
    html_text = legacy_style.sub('\n', html_text)
    return legacy_script.sub('\n', html_text)


def _remove_legacy_speech_controls(html_text: str) -> str:
    button_row = r'<div\b[^>]*class\s*=\s*["\'][^"\']*\bbutton-row\b[^"\']*["\'][^>]*>'
    stop_pattern = re.compile(
        rf'(?is)\s*{button_row}\s*<button\b[^>]*>.*?音声を止める.*?</button>\s*</div>\s*'
    )
    explanation_pattern = re.compile(
        rf'(?is)\s*{button_row}\s*<button\b[^>]*>.*?かいせつを再生.*?</button>\s*</div>\s*'
    )
    html_text = stop_pattern.sub('\n', html_text)
    return explanation_pattern.sub('\n', html_text)


def _restore_body_intro(html_text: str) -> str:
    body_match = re.search(r'<body\b[^>]*>', html_text, re.IGNORECASE)
    heading_match = re.search(r'<h1\b[^>]*>', html_text, re.IGNORECASE)
    if not body_match or not heading_match or heading_match.start() <= body_match.end():
        return html_text

    intro_start = body_match.end()
    intro_end = heading_match.start()
    intro = html_text[intro_start:intro_end]
    fragments: list[tuple[int, int, str]] = []

    back_match = re.search(
        r'<a\b[^>]*class\s*=\s*["\'][^"\']*\bback-link\b[^"\']*["\'][^>]*>.*?</a>',
        intro,
        re.IGNORECASE | re.DOTALL,
    )
    if back_match:
        fragments.append((back_match.start(), back_match.end(), back_match.group(0).strip()))

    video_match = re.search(
        r'<div\b[^>]*class\s*=\s*["\'][^"\']*\bvideo-panel\b[^"\']*["\'][^>]*>',
        intro,
        re.IGNORECASE,
    )
    if video_match:
        balanced_video = _find_balanced_div(intro, video_match.start())
        if balanced_video:
            video_start, video_end = balanced_video
            fragments.append((video_start, video_end, intro[video_start:video_end].strip()))

    fragments.sort(key=lambda fragment: fragment[0])
    preserved_intro = '\n'.join(fragment[2] for fragment in fragments)
    return html_text[:intro_start] + ('\n' + preserved_intro + '\n' if preserved_intro else '\n') + html_text[heading_match.start():]


def clean_experience_markup(html_text: str) -> str:
    for marker_name in GENERATED_MARKERS:
        html_text = _remove_marked_block(html_text, marker_name)
    html_text = _clean_legacy_experience_assets(html_text)
    html_text = _remove_legacy_speech_controls(html_text)
    return _restore_body_intro(html_text)


def _javascript_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _build_text_size_controls() -> str:
    return '''<!-- TEXT_SIZE_CONTROLS_START -->
    <div class="text-size-controls" data-text-size-controls>
      <span class="text-size-label" data-text-size-label>文字の大きさ：標準</span>
      <button type="button" class="text-size-toggle" data-text-size-toggle aria-label="文字の大きさを変更（現在は標準）">🔤 文字を大きくする</button>
    </div>
    <!-- TEXT_SIZE_CONTROLS_END -->'''


def _insert_text_size_controls(html_text: str, filename: str) -> str:
    html_text = _remove_marked_block(html_text, 'TEXT_SIZE_CONTROLS')
    controls = _build_text_size_controls()

    if filename == 'import random.html':
        html_text = html_text.replace(
            '<div id="selectScreen" class="screen">',
            f'<div id="selectScreen" class="screen">\n{controls}',
            1,
        )
        return html_text.replace(
            '<div id="gameScreen" class="screen hidden">',
            f'<div id="gameScreen" class="screen hidden">\n{controls}',
            1,
        )

    body_match = re.search(r'<body\b[^>]*>', html_text, re.IGNORECASE)
    if not body_match:
        return html_text
    return html_text[:body_match.end()] + f'\n{controls}' + html_text[body_match.end():]


def _build_speech_controls(explanation: str) -> str:
    return f'''<!-- SPEECH_CONTROLS_START -->
    <div class="button-row speech-controls" aria-label="音声の操作">
      <button type="button" class="action-btn" onclick='yomu({_javascript_string(explanation)})'>📣 かいせつを再生</button>
      <button type="button" class="action-btn stop-btn" onclick="tomeru()">⏹️ 音声を止める</button>
    </div>
    <!-- SPEECH_CONTROLS_END -->'''


def _build_experience_styles() -> str:
    return '''<!-- EXPERIENCE_STYLES_START -->
    <style>
      .experience-panel {
        background: linear-gradient(135deg, #fff7d9, #f3f9ff);
        border: 3px solid #d79b2f;
        border-radius: 18px;
        padding: 18px 18px 10px;
        margin: 18px 0 20px;
        box-shadow: 0 8px 18px rgba(87, 76, 0, 0.12);
      }
      .experience-status {
        font-size: 1.05rem;
        font-weight: 800;
        color: #7a4b00;
        margin-bottom: 8px;
      }
      .experience-panel h2 {
        margin: 6px 0 12px;
      }
      .experience-steps {
        display: grid;
        gap: 10px;
        margin: 0 0 12px;
      }
      .experience-step {
        background: #fff;
        border: 2px solid #e5d6a7;
        border-radius: 12px;
        padding: 12px 14px;
        font-weight: 700;
        color: #3a3a3a;
        transition: all 0.15s ease;
      }
      .experience-step.active {
        background: #eaf7ff;
        border-color: #1e5bd7;
        box-shadow: inset 0 0 0 2px rgba(30, 91, 215, 0.25);
      }
      .experience-step.done {
        background: #ebfce9;
        border-color: #5aa16e;
      }
      @media (max-width: 600px) {
        .experience-panel { padding: 16px 12px 8px; }
      }
    </style>
    <!-- EXPERIENCE_STYLES_END -->'''


def _ensure_theme_link(html_text: str) -> str:
    theme_link_pattern = rf'<link\b[^>]*href\s*=\s*["\']{re.escape(THEME_STYLESHEET)}["\'][^>]*>'
    if re.search(theme_link_pattern, html_text, re.IGNORECASE):
        return html_text

    return html_text.replace(
        '</head>',
        f'  <link rel="stylesheet" href="{THEME_STYLESHEET}">\n</head>',
        1,
    )


def _ensure_theme_script(html_text: str) -> str:
    script_pattern = rf'<script\b[^>]*src\s*=\s*["\']{re.escape(THEME_SCRIPT)}["\'][^>]*>\s*</script>'
    if re.search(script_pattern, html_text, re.IGNORECASE):
        return html_text

    return html_text.replace(
        '</body>',
        f'  <script src="{THEME_SCRIPT}"></script>\n</body>',
        1,
    )


def _ensure_brain_training_script(html_text: str, filename: str) -> str:
    if filename != 'noutore.html':
        return html_text

    script_pattern = rf'<script\b[^>]*src\s*=\s*["\']{re.escape(BRAIN_TRAINING_SCRIPT)}["\'][^>]*>\s*</script>'
    if re.search(script_pattern, html_text, re.IGNORECASE):
        return html_text

    return html_text.replace(
        '</body>',
        f'  <script src="{BRAIN_TRAINING_SCRIPT}"></script>\n</body>',
        1,
    )


def _ensure_body_class(html_text: str, body_class: str) -> str:
    html_text = re.sub(
        r'<body(?P<attribute>class\s*=)',
        r'<body \g<attribute>',
        html_text,
        count=1,
        flags=re.IGNORECASE,
    )
    body_match = re.search(r'<body\b([^>]*)>', html_text, re.IGNORECASE)
    if not body_match:
        return html_text

    attributes = body_match.group(1)
    class_match = re.search(
        r'(?P<leading>\s+)class\s*=\s*(?P<quote>["\'])(?P<classes>.*?)(?P=quote)',
        attributes,
        re.IGNORECASE | re.DOTALL,
    )
    if class_match:
        classes = class_match.group('classes').split()
        if body_class not in classes:
            classes.append(body_class)
        replacement = (
            f"{class_match.group('leading')}class={class_match.group('quote')}"
            f"{' '.join(classes)}{class_match.group('quote')}"
        )
        attributes = attributes[:class_match.start()] + replacement + attributes[class_match.end():]
    else:
        attributes = f'{attributes} class="{body_class}"'

    return html_text[:body_match.start(1)] + attributes + html_text[body_match.end(1):]


def _build_experience_script(steps: list[str]) -> str:
    serialized_steps = json.dumps(steps, ensure_ascii=False)
    return f'''<!-- EXPERIENCE_SCRIPT_START -->
    <script>
      (function () {{
        const stepList = {serialized_steps};
        let experienceIndex = 0;

        function updateCaption(text) {{
          const caption = document.getElementById('video-caption');
          if (caption) {{
            caption.textContent = text || '説明を待っています';
          }}
        }}

        function yomu(text) {{
          updateCaption(text);
          if (!('speechSynthesis' in window)) {{
            return;
          }}

          window.speechSynthesis.cancel();
          const speech = new SpeechSynthesisUtterance(text || '説明を待っています');
          speech.lang = 'ja-JP';
          speech.rate = 1;
          speech.pitch = 1;
          speech.volume = 1;
          window.speechSynthesis.speak(speech);
        }}

        function tomeru() {{
          if ('speechSynthesis' in window) {{
            window.speechSynthesis.cancel();
          }}
          updateCaption('音声を止めました');
        }}

        function renderExperience() {{
          const panel = document.getElementById('experience-panel');
          if (!panel) {{
            return;
          }}

          const steps = panel.querySelectorAll('.experience-step');
          steps.forEach((node, index) => {{
            node.classList.toggle('active', index === experienceIndex);
            node.classList.toggle('done', index < experienceIndex);
          }});

          const status = panel.querySelector('.experience-status');
          if (status) {{
            status.textContent = '体験ステップ ' + (experienceIndex + 1) + ' / ' + stepList.length;
          }}

          const currentStep = stepList[experienceIndex];
          if (currentStep) {{
            yomu(currentStep);
          }}
        }}

        function nextExperienceStep() {{
          if (experienceIndex < stepList.length - 1) {{
            experienceIndex += 1;
            renderExperience();
            return;
          }}

          const panel = document.getElementById('experience-panel');
          const status = panel && panel.querySelector('.experience-status');
          if (status) {{
            status.textContent = '体験完了！ すべての手順を確認しました';
          }}
        }}

        function resetExperience() {{
          experienceIndex = 0;
          renderExperience();
        }}

        window.__EXPERIENCE_STEPS__ = stepList;
        window.nextExperienceStep = nextExperienceStep;
        window.resetExperience = resetExperience;
        window.yomu = yomu;
        window.tomeru = tomeru;
        window.addEventListener('DOMContentLoaded', renderExperience, {{ once: true }});
      }}());
    </script>
    <!-- EXPERIENCE_SCRIPT_END -->'''


def inject_experience_block(html_text: str, filename: str) -> str:
    html_text = clean_experience_markup(html_text)
    html_text = _ensure_theme_link(html_text)
    page_class = 'game-page' if filename == 'import random.html' else 'topic-page'
    html_text = _ensure_body_class(html_text, page_class)
    html_text = _insert_text_size_controls(html_text, filename)
    html_text = _ensure_theme_script(html_text)
    html_text = _ensure_brain_training_script(html_text, filename)
    steps = experience_steps.get(filename)
    if not steps:
        return html_text

    speech_controls = ''
    if filename in explanations:
        speech_controls = _build_speech_controls(explanations[filename])

    styles = _build_experience_styles()
    html_text = html_text.replace('</head>', f'{styles}\n</head>', 1)

    markup = build_experience_markup(steps)
    heading_match = re.search(r'<h1\b[^>]*>', html_text, re.IGNORECASE)
    if heading_match:
        insertion_point = heading_match.start()
        intro_blocks = '\n'.join(block for block in (speech_controls, markup) if block)
        html_text = html_text[:insertion_point] + intro_blocks + '\n    ' + html_text[insertion_point:]

    script = _build_experience_script(steps)
    html_text = html_text.replace('</body>', f'{script}\n</body>', 1)
    return html_text


def main() -> None:
    for path in sorted(ROOT.glob('*.html')):
        text = path.read_text(encoding='utf-8')
        if path.name == 'index.html':
            new_text = _ensure_body_class(_ensure_theme_link(text), 'index-page')
            new_text = _insert_text_size_controls(new_text, path.name)
            new_text = _ensure_theme_script(new_text)
        else:
            new_text = inject_experience_block(text, path.name)

        if new_text != text:
            path.write_text(new_text, encoding='utf-8')
            print(f'updated {path.name}')
        else:
            print(f'no changes for {path.name}')

    print('done')


if __name__ == '__main__':
    main()
