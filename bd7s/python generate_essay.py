import pandas as pd
import re

# 이모지 시퀀스 패턴: 기본 이모지 + 피부색/ZWJ 연속 문자까지 하나의 그룹으로 포착
# (예: 🫶🏻, ❤️‍🔥, ⭐️ 등 복합 시퀀스 포함)
EMOJI_RE = re.compile(
    r'(?:[\U00010000-\U0010FFFF]|'           # 보조 평면 문자 (대부분의 이모지)
    r'[\u2600-\u27BF]|'                       # 기타 기호 + 딩뱃
    r'[\u2B50\u2B55]|'                        # ⭐ ⭕ 등
    r'[\u25AA-\u25FE]|'                       # 기하 도형
    r'[\u24C2\u3297\u3299])'                  # 둘러싸인 문자
    r'(?:[\uFE00-\uFE0F\u200D\U00010000-\U0010FFFF])*',  # 변이선택자/ZWJ/후속 이모지
    re.UNICODE
)

def escape_latex(text):
    """
    리뷰 내용 중에 LaTeX 컴파일 에러를 일으키는 특수문자가 있을 경우,
    안전하게 출력될 수 있도록 이스케이프(\) 처리해 주는 함수입니다.
    """
    if pd.isna(text):
        return ""
    text = str(text)

    # 역슬래시(\)를 가장 먼저 처리해야 다른 기호 처리와 꼬이지 않습니다.
    text = text.replace('\\', r'\textbackslash{}')
    
    escape_map = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}'
    }
    
    for char, escaped in escape_map.items():
        text = text.replace(char, escaped)
    
    # [수정된 부분] 엑셀의 줄바꿈(\n)을 LaTeX의 안전한 문단 나눔(\par)으로 변경
    # 엔터를 여러 번 쳤더라도 에러가 나지 않고, 약간의 여백(\vspace)을 주어 감성적으로 띄워줍니다.
    text = re.sub(r'\n+', r' \\par ', text)

    # 이모지를 이모지 전용 폰트로 감싸기
    # 보조 평면(U+10000+) 문자가 포함된 시퀀스 → \coloremoji (Segoe UI Emoji)
    # BMP 기호(♡, ★ 등)만으로 이루어진 시퀀스 → \emojifont (Segoe UI Symbol)
    def emoji_replace(m):
        seq = m.group()
        if any(ord(c) >= 0x10000 for c in seq):
            return r'{\coloremoji ' + seq + r'}'
        return r'{\emojifont ' + seq + r'}'

    text = EMOJI_RE.sub(emoji_replace, text)

    return text

# 1. 통합 엑셀 파일 불러오기
try:
    df = pd.read_excel("all_platforms_reviews.xlsx")
except FileNotFoundError:
    print("엑셀 파일을 찾을 수 없습니다. 파일명을 확인해주세요.")
    exit()

# 빈 객실명 데이터 처리 (NaN -> '객실 정보 없음')
df['객실명'] = df['객실명'].fillna('객실 정보 없음')

# 2. LaTeX 문서 뼈대 (앞부분: 헤더 및 표지) 설정
# 파이썬의 raw string(r"")을 사용하여 LaTeX의 백슬래시들을 그대로 유지합니다.
latex_header = r"""\documentclass[10pt, a5paper]{article}

% --- UNIVERSAL PREAMBLE BLOCK ---
\usepackage[a5paper, top=3cm, bottom=3cm, left=1.5cm, right=1.5cm]{geometry}
\pagestyle{empty}
\usepackage{fontspec}

\usepackage[korean, bidi=basic, provide=*]{babel}

\babelprovide[import, onchar=ids fonts]{korean}
\babelprovide[import, onchar=ids fonts]{english}

\babelfont{rm}{Noto Serif}
\babelfont[korean]{rm}{Noto Serif KR}
\tracinglostchars=0

\newfontfamily\emojifont{Segoe UI Symbol}
\newfontfamily\coloremoji{Segoe UI Emoji}

\usepackage{changepage}
\usepackage{enumitem}
\setlist[itemize]{label=-}

\usepackage{xcolor}
\usepackage{setspace}
\usepackage{etoolbox}
\usepackage{tikz}

\definecolor{covergold}{HTML}{E5C158}
\definecolor{separatorstar}{HTML}{D4AF37}

% ==========================================
% 1. 네이버 리뷰: 가운데 점(·)
\newcommand{\naverreview}[4]{
    \vspace{0.3cm}
    \begin{adjustwidth}{0.05\textwidth}{0.05\textwidth}
        {\normalsize \setstretch{1.2} \raggedright ``#4''\par}
        \vspace{1.2em}
        \hfill {\small \color{gray} #2 \quad · \quad
        \ifstrequal{#3}{객실 정보 없음}{}{\ifstrempty{#3}{}{#3 \quad · \quad }}#1}\par
    \end{adjustwidth}
    \vspace{1cm}
    \centerline{\color{separatorstar} ★}
    \vspace{0.7cm}
}

% 2. 야놀자 리뷰: 수직선(|)
\newcommand{\yanoljareview}[4]{
    \vspace{0.3cm}
    \begin{adjustwidth}{0.05\textwidth}{0.05\textwidth}
        {\normalsize \setstretch{1.2} \raggedright ``#4''\par}
        \vspace{1.2em}
        \hfill {\small \color{gray} #2 \quad $\vert$ \quad
        \ifstrequal{#3}{객실 정보 없음}{}{\ifstrempty{#3}{}{#3 \quad $\vert$ \quad }}#1}\par
    \end{adjustwidth}
    \vspace{1cm}
    \centerline{\color{separatorstar} ★}
    \vspace{0.7cm}
}

% 3. 여기어때 리뷰: 슬래시(/)
\newcommand{\yeogireview}[4]{
    \vspace{0.3cm}
    \begin{adjustwidth}{0.05\textwidth}{0.05\textwidth}
        {\normalsize \setstretch{1.2} \raggedright ``#4''\par}
        \vspace{1.2em}
        \hfill {\small \color{gray} #2 \quad / \quad
        \ifstrequal{#3}{객실 정보 없음}{}{\ifstrempty{#3}{}{#3 \quad / \quad }}#1}\par
    \end{adjustwidth}
    \vspace{1cm}
    \centerline{\color{separatorstar} ★}
    \vspace{0.7cm}
}

\begin{document}

% --- 타이틀 페이지 (북커버 디자인) ---
\begin{titlepage}
    \vspace*{1.5cm}
    \begin{center}
    \begin{tikzpicture}[scale=0.9]
        \coordinate (S1) at (0,0);
        \coordinate (S2) at (1.5, -0.5);
        \coordinate (S3) at (3, 0);
        \coordinate (S4) at (4, -1.2);
        \coordinate (S5) at (4.5, -3);
        \coordinate (S6) at (6.5, -3.5);
        \coordinate (S7) at (7, -1.5);
        \draw[covergold!80, thick, dashed] (S1) -- (S2) -- (S3) -- (S4) -- (S5) -- (S6) -- (S7) -- (S4);
        \foreach \p in {S1,S2,S3,S4,S5,S6,S7} {
            \fill[covergold] (\p) circle (3.5pt);
            \fill[white] (\p) circle (1.5pt);
        }
    \end{tikzpicture}
    \end{center}
    
    \vspace*{1.5cm}
    \begin{center}
        {\color{covergold} \Large 북두칠성 별자리 아래,}\\[0.8cm]
        {\color{black} \Huge \textbf{따뜻했던 시간들}}\\[1.0cm]
        {\color{darkgray} \large 우리가 머문 자리, 그곳에 남겨진 이야기}\\[1.5cm]
        \vfill
        {\color{darkgray} \normalsize 가평 북두칠성 글램핑} \\[0.3cm]
        {\color{darkgray} \small 2026 고객 리뷰 에세이집}
        \vspace*{1cm}
    \end{center}
\end{titlepage}

\newpage
\vspace*{0.5cm}
"""

# 3. 엑셀 데이터를 돌면서 리뷰 블록 자동 생성
latex_body = ""

for index, row in df.iterrows():
    platform = row['플랫폼']
    date = escape_latex(row['작성일자'])
    user_id = escape_latex(row['아이디'])
    room = escape_latex(row['객실명'])
    content = escape_latex(row['리뷰내용'])
    
    # 플랫폼별로 사용할 LaTeX 명령어 결정
    if platform == '네이버':
        macro_name = "naverreview"
    elif platform == '야놀자':
        macro_name = "yanoljareview"
    elif platform == '여기어때':
        macro_name = "yeogireview"
    else:
        # 혹시 모를 기타 데이터는 기본적으로 네이버 서식을 따르게 함
        macro_name = "naverreview"
        
    # f-string을 활용하여 명령어 조합
    # 형태: \naverreview{날짜}{아이디}{객실명}{내용}
    latex_body += f"\\{macro_name}\n"
    latex_body += f"{{{date}}}\n"
    latex_body += f"{{{user_id}}}\n"
    latex_body += f"{{{room}}}\n"
    latex_body += f"{{{content}}}\n\n"

# 4. 문서 닫기
latex_footer = r"\end{document}"

# 5. 합치기 및 .tex 파일로 저장
final_latex_code = latex_header + latex_body + latex_footer

output_filename = "review_essay_2026.tex"
with open(output_filename, "w", encoding="utf-8") as f:
    f.write(final_latex_code)

print("✅ 자동 변환 완료!")
print(f"총 {len(df)}개의 리뷰가 담긴 '{output_filename}' 파일이 생성되었습니다.")
print("이 파일을 LaTeX 컴파일러(예: Overleaf, Texmaker)에 붙여넣기만 하면 에세이집 PDF가 완성됩니다!")