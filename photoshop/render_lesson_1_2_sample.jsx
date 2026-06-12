#target photoshop
app.displayDialogs = DialogModes.NO;

var ROOT = "C:/Users/Administrator/Desktop/中级美语";
var OUT = ROOT + "/output/lesson_1_2_sample";
var START_LESSON_INDEX = 0;
var END_LESSON_INDEX = 0;
var MAX_PAGES_PER_LESSON = 20;
var RENDER_FIRST_PAGE_ONLY = true;
var DATA = {
  "lessonNo": "Lesson 1-2",
  "lessonTitle": "Rome Wasn't Built in a Day",
  "part1Title": "PART 1    Reading&Dialogue",
  "part2Title": "PART 2    Vocabulary&Idioms",
  "part3Title": "PART 3    Grammar points",
  "part4Title": "PART 4    Exercise",
  "readingLines": [
    {
      "kind": "phonetic",
      "text": "[ɪntɚˈnæʃənl] [ˈlæŋɡwɪdʒ]"
    },
    {
      "kind": "body",
      "text": "English is an international language. Therefore, it is necessary for"
    },
    {
      "kind": "phonetic",
      "text": "[rɪˈwɔrdɪŋ]"
    },
    {
      "kind": "body",
      "text": "us to learn it. It can be rewarding or just a waste of time. It's up to you. It"
    },
    {
      "kind": "phonetic",
      "text": "[dɪˈpɛndz ɑn] [tɪps]"
    },
    {
      "kind": "body",
      "text": "depends on how you study it. Here are some tips about learning English."
    },
    {
      "kind": "phonetic",
      "text": "[əˈfred]"
    },
    {
      "kind": "body",
      "text": "First, don't be afraid to make mistakes. You will learn from them."
    },
    {
      "kind": "phonetic",
      "text": "[ʃaɪ] [ˌθɪkˈskɪnd] [spik ʌp]"
    },
    {
      "kind": "body",
      "text": "Second, you must not be shy. Be thick-skinned and speak up! Finally,"
    },
    {
      "kind": "phonetic",
      "text": "[ˈpeʃənt]"
    },
    {
      "kind": "body",
      "text": "you must be patient. Remember, \"Rome wasn't built in a day.\""
    }
  ],
  "readingBlocks": [
    {
      "phonetic": "[ɪntɚˈnæʃənl] [ˈlæŋɡwɪdʒ]",
      "text": "English is an international language. Therefore, it is necessary for",
      "segments": [
        {
          "text": "[ɪntɚˈnæʃənl]",
          "target": "international",
          "vocabWord": "international"
        },
        {
          "text": "[ˈlæŋɡwɪdʒ]",
          "target": "language",
          "vocabWord": "language"
        }
      ]
    },
    {
      "phonetic": "[rɪˈwɔrdɪŋ]",
      "text": "us to learn it. It can be rewarding or just a waste of time. It's up to you. It",
      "segments": [
        {
          "text": "[rɪˈwɔrdɪŋ]",
          "target": "rewarding",
          "vocabWord": "rewarding"
        }
      ]
    },
    {
      "phonetic": "[dɪˈpɛndz ɑn] [tɪps]",
      "text": "depends on how you study it. Here are some tips about learning English.",
      "segments": [
        {
          "text": "[dɪˈpɛndz ɑn]",
          "target": "depends on",
          "vocabWord": "depend on"
        },
        {
          "text": "[tɪps]",
          "target": "tips",
          "vocabWord": "tip"
        }
      ]
    },
    {
      "phonetic": "[əˈfred]",
      "text": "First, don't be afraid to make mistakes. You will learn from them.",
      "segments": [
        {
          "text": "[əˈfred]",
          "target": "afraid",
          "vocabWord": "afraid"
        }
      ]
    },
    {
      "phonetic": "[ʃaɪ] [ˌθɪkˈskɪnd] [spik ʌp]",
      "text": "Second, you must not be shy. Be thick-skinned and speak up! Finally,",
      "segments": [
        {
          "text": "[ʃaɪ]",
          "target": "shy",
          "vocabWord": "shy"
        },
        {
          "text": "[ˌθɪkˈskɪnd]",
          "target": "thick-skinned",
          "vocabWord": "thick-skinned"
        },
        {
          "text": "[spik ʌp]",
          "target": "speak up",
          "vocabWord": "speak up"
        }
      ]
    },
    {
      "phonetic": "[ˈpeʃənt]",
      "text": "you must be patient. Remember, \"Rome wasn't built in a day.\"",
      "segments": [
        {
          "text": "[ˈpeʃənt]",
          "target": "patient",
          "vocabWord": "patient"
        }
      ]
    }
  ],
  "readingLeft": "[ɪntɚˈnæʃənl] [ˈlæŋɡwɪdʒ]\rEnglish is an international language. Therefore, it is necessary for\r[rɪˈwɔrdɪŋ]\rus to learn it. It can be rewarding or just a waste of time. It's up to you. It\r[dɪˈpɛndz ɑn] [tɪps]\rdepends on how you study it. Here are some tips about learning English.\r[əˈfred]\rFirst, don't be afraid to make mistakes. You will learn from them.",
  "readingRight": "[ʃaɪ] [ˌθɪkˈskɪnd] [spik ʌp]\rSecond, you must not be shy. Be thick-skinned and speak up! Finally,\r[ˈpeʃənt]\ryou must be patient. Remember, \"Rome wasn't built in a day.\"",
  "readingMetrics": {
    "source": {
      "readingLayers": "D:\\Documents\\New project\\probes\\probe_psd_reading_layers.json",
      "textStyleRanges": "D:\\Documents\\New project\\probes\\probe_psd_text_style_ranges.json",
      "paragraphStyle": "D:\\Documents\\New project\\probes\\probe_psd_reading_paragraph_style.json"
    },
    "textX": 300,
    "textTop": 857,
    "maxRight": 2109,
    "lineGap": 68.75,
    "bodyFirstLineIndent": 31.0000012207031,
    "bodyContinuationIndent": 0,
    "blockLineCount": 3,
    "phoneticStyleSource": "@PART1_READING_LEFT_TEXT_STYLE_SOURCE",
    "bodyStyleSource": "@PART1_DIALOGUE_INTRO_TEXT"
  },
  "dialogueIntro": "Mack is talking to his friend Don.",
  "dialogueRole": "(M = Mack; D = Don)",
  "dialogueLines": [
    {
      "kind": "phonetic",
      "text": "[haɪ]"
    },
    {
      "kind": "dialogue",
      "speaker": "M",
      "text": "M: Hi, Don! How are you doing in your English class."
    },
    {
      "kind": "dialogue",
      "speaker": "D",
      "text": "D: Not so well, I'm afraid."
    },
    {
      "kind": "dialogue",
      "speaker": "D",
      "text": "D: I'm not improving. Tell me, how come your English is so good?"
    },
    {
      "kind": "dialogue",
      "speaker": "M",
      "text": "M: Hey, come back! I was just kidding."
    }
  ],
  "dialogue": "[haɪ]\rM: Hi, Don! How are you doing in your English class.\rD: Not so well, I'm afraid.\rD: I'm not improving. Tell me, how come your English is so good?\rM: Hey, come back! I was just kidding.",
  "dialogueMetrics": {
    "source": {
      "dialogue": "D:\\Documents\\New project\\probes\\probe_psd_dialogue_metrics.json",
      "phonetic": "D:\\Documents\\New project\\probes\\probe_psd_phonetic_metrics.json",
      "dialogueTextSource": "@PART1_READING_RIGHT_TEXT_STYLE_SOURCE"
    },
    "roleX": 2831,
    "lineTop": 539.3333435058594,
    "lineGap": 83.3333435058594,
    "roleWidths": {
      "M:": 55,
      "D:": 47
    },
    "roleSpaceWidth": 12,
    "textMaxRight": 4667,
    "continuationIndentX": 2898,
    "lineBgBottom": 1433,
    "phoneticOffset": 71
  },
  "vocab": [
    {
      "no": "1",
      "word": "international",
      "phonetic": "KK: [ˌɪntɚˈnæʃənl]\rIPA: [ˌɪntərˈnæʃənəl]",
      "meaning": "adj. 国际性的；国际间的"
    },
    {
      "no": "2",
      "word": "language",
      "phonetic": "KK: [ˈlæŋɡwɪdʒ]\rIPA: [ˈlæŋɡwɪdʒ]",
      "meaning": "n. 语言（可数）；言词（不可数）"
    },
    {
      "no": "3",
      "word": "rewarding",
      "phonetic": "KK: [rɪˈwɔrdɪŋ]\rIPA: [rɪˈwɔːrdɪŋ]",
      "meaning": "adj. 有（获）益的；值得做的；划算的"
    },
    {
      "no": "4",
      "word": "depend on",
      "phonetic": "KK: [dɪˈpɛnd ɑn]\rIPA: [dɪˈpend ɑːn]",
      "meaning": "视……而定"
    },
    {
      "no": "5",
      "word": "tip",
      "phonetic": "KK: [tɪp]\rIPA: [tɪp]",
      "meaning": "n. 建议；小费"
    },
    {
      "no": "6",
      "word": "afraid",
      "phonetic": "KK: [əˈfred]\rIPA: [əˈfreɪd]",
      "meaning": "adj. 害怕的；恐惧的"
    },
    {
      "no": "7",
      "word": "be afraid to +动词原形",
      "phonetic": "KK: [bi əˈfred tu]\rIPA: [bi əˈfreɪd tu]",
      "meaning": "害怕去做……"
    },
    {
      "no": "8",
      "word": "shy",
      "phonetic": "KK: [ʃaɪ]\rIPA: [ʃaɪ]",
      "meaning": "adj. 羞怯的"
    },
    {
      "no": "9",
      "word": "thick-skinned",
      "phonetic": "KK: [ˌθɪkˈskɪnd]\rIPA: [ˌθɪkˈskɪnd]",
      "meaning": "adj. 厚脸皮的"
    },
    {
      "no": "10",
      "word": "speak up",
      "phonetic": "KK: [spik ʌp]\rIPA: [spiːk ʌp]",
      "meaning": "大声说话；开口说出来"
    },
    {
      "no": "11",
      "word": "patient",
      "phonetic": "KK: [ˈpeʃənt]\rIPA: [ˈpeɪʃənt]",
      "meaning": "adj. 有耐心的（常与介词 with连用）"
    },
    {
      "no": "12",
      "word": "improve",
      "phonetic": "KK: [ɪmˈpruv]\rIPA: [ɪmˈpruːv]",
      "meaning": "vt. & vi.（使）进步；改善"
    },
    {
      "no": "13",
      "word": "hi",
      "phonetic": "KK: [haɪ]\rIPA: [haɪ]",
      "meaning": "int. 嗨（打招呼声）"
    },
    {
      "no": "14",
      "word": "kid",
      "phonetic": "KK: [kɪd]\rIPA: [kɪd]",
      "meaning": "vt. & vi.（口语）（与……）开玩笑 & n. 小孩"
    }
  ],
  "grammarLead": "本节课主要学习特殊疑问词引导的名词性从句。",
  "grammarP2A": "对于特殊疑问句，我们只需要把特殊疑问词后面倒装的句子还原成正常的语序就可以当名词性从句用了，比如：",
  "grammarP2B": "What is your name? 变从句 → what your name is. be动词回到主语后面",
  "grammarP3A": "Where will Vicky go? 变从句 → where Vicky will go. 助动词（can，will，have等）回到主语后面，这类助动词要么本身是情态动词，有确切的意思，修饰谓语动词，要么是为了帮助构成时态，变回陈述句语序后，其意思和时态都不变，因此仍然需要这些词，不能省掉。",
  "grammarP3B": "Why does Vicky like kids? 变从句 → why Vicky likes kids. 助动词（do，does，did等）去除，动词还原成应有的时态，这里为一般现在时，所以动词要用三单。这类助动词只是为了帮助构成特殊疑问句，变从句后原来的句子还原成陈述句语序了，不再是特殊疑问句了，所以要将助动词去掉。",
  "grammarP3C": "例子：",
  "grammarP3D": "①What your name is doesn't matter to me. 名词性从句作主语",
  "grammarP4A": "②The question is where Vicky will go. 名词性从句作表语",
  "grammarP4B": "③I don't know why Vicky likes kids. 名词性从句作动词的宾语",
  "grammarOverflow": [
    "④We are talking about where Vicky will go. 名词性从句作介词的宾语"
  ],
  "exerciseSection1No": "1.",
  "exerciseSection2No": "2.",
  "exerciseP4A": "1. 从下列句子中找出名词性从句，在从句下方画横线。\r① What he needs is more time.\r② What you learn will help you later.\r③ This is what I have been looking for.\r④ Life is what you make it.\r⑤ I can't remember what she told me.\r⑥ He didn't understand what I meant.\r⑦ She finally realized what her mistake was.",
  "exerciseP4B": "⑧ We are worried about what will happen next.\r⑨ She cares about what others think of her.\r⑩ They are talking about what happened yesterday.\r2. 翻译\r① 我不知道如何提高我的国际语言水平。（international language）\r____________________________________________\r② 他告诉我的是一些很有用的建议。（useful）\r____________________________________________\r③ 问题是我们为什么要学得脸皮厚一点。（problem; thick-skinned）\r____________________________________________\r④ 我明白了什么才是真正值得做的事。（worthy）\r____________________________________________\r⑤ 她害怕别人会怎么看她。（be afraid to）\r____________________________________________\r⑥ 他在问我这些语言技巧来自哪里。（language skills）\r____________________________________________\r⑦ 成功的关键是你是否愿意不断进步。（success; key; improve）\r____________________________________________\r⑧ 我们正在讨论怎样学习国际语言才更有效。（effectively）\r____________________________________________\r⑨ 他只是在开玩笑，这就是我想说的。（kid）\r____________________________________________\r⑩ 你有多耐心决定了你能进步多快。（patient; decide; improve）\r____________________________________________"
};
var PLAN = {
  "lessonNo": "Lesson 1-2",
  "lessonTitle": "Rome Wasn't Built in a Day",
  "status": "planOnlyNotRendered",
  "rules": {
    "preserveHiddenTemplateLayers": true,
    "partTitlesPreserveTemplateStyle": true,
    "vocabRowHeight": "fixed",
    "vocabLongText": "wrapInsideFixedTextBoxOrFlagReview",
    "part3NoFakeSubtitles": true,
    "exerciseKeepOriginalNumbering": true,
    "pageNumberFormat": "000"
  },
  "pages": [
    {
      "pageIndex": 1,
      "template": "3-4 1.psd",
      "pageNumbers": [
        "001",
        "002"
      ],
      "frames": {
        "left": {
          "top": 649,
          "left": 200,
          "bottom": 3311,
          "right": 2149
        },
        "right": {
          "top": 421,
          "left": 2773,
          "bottom": 3311,
          "right": 4840
        },
        "source": "hidden PSD reference layers; keep hidden in output"
      },
      "hiddenLayers": [
        "@SHELL_CONTENT_PANEL_DECOR_SHAPE",
        "@SHELL_CONTENT_PANEL_LEFT",
        "@SHELL_CONTENT_PANEL_RIGHT",
        "@SHELL_PANEL_CORNER_DECOR_RIGHT",
        "@SHELL_PANEL_CORNER_DECOR_LEFT"
      ],
      "modules": [
        {
          "id": "part1",
          "type": "readingDialogue",
          "dynamic": true,
          "titleLayerPolicy": "preserveTemplateTitleLayer",
          "reading": {
            "styleSources": [
              "@PART1_READING_LEFT_TEXT_STYLE_SOURCE",
              "@PART1_READING_RIGHT_TEXT_STYLE_SOURCE"
            ],
            "lines": [
              {
                "kind": "phonetic",
                "text": "[ɪntɚˈnæʃənl] [ˈlæŋɡwɪdʒ]"
              },
              {
                "kind": "body",
                "text": "English is an international language. Therefore, it is necessary for"
              },
              {
                "kind": "phonetic",
                "text": "[rɪˈwɔrdɪŋ]"
              },
              {
                "kind": "body",
                "text": "us to learn it. It can be rewarding or just a waste of time. It's up to you. It"
              },
              {
                "kind": "phonetic",
                "text": "[dɪˈpɛndz ɑn] [tɪps]"
              },
              {
                "kind": "body",
                "text": "depends on how you study it. Here are some tips about learning English."
              },
              {
                "kind": "phonetic",
                "text": "[əˈfred]"
              },
              {
                "kind": "body",
                "text": "First, don't be afraid to make mistakes. You will learn from them."
              },
              {
                "kind": "phonetic",
                "text": "[ʃaɪ] [ˌθɪkˈskɪnd] [spik ʌp]"
              },
              {
                "kind": "body",
                "text": "Second, you must not be shy. Be thick-skinned and speak up! Finally,"
              },
              {
                "kind": "phonetic",
                "text": "[ˈpeʃənt]"
              },
              {
                "kind": "body",
                "text": "you must be patient. Remember, \"Rome wasn't built in a day.\""
              }
            ],
            "requiresPsMeasurement": [
              "line wraps",
              "phonetic y offset",
              "green border bottom"
            ]
          },
          "dialogue": {
            "intro": "Mack is talking to his friend Don.",
            "roleNote": "(M = Mack; D = Don)",
            "lines": [
              {
                "kind": "phonetic",
                "text": "[haɪ]"
              },
              {
                "kind": "dialogue",
                "speaker": "M",
                "text": "M: Hi, Don! How are you doing in your English class."
              },
              {
                "kind": "dialogue",
                "speaker": "D",
                "text": "D: Not so well, I'm afraid."
              },
              {
                "kind": "dialogue",
                "speaker": "D",
                "text": "D: I'm not improving. Tell me, how come your English is so good?"
              },
              {
                "kind": "dialogue",
                "speaker": "M",
                "text": "M: Hey, come back! I was just kidding."
              }
            ],
            "requiresPsMeasurement": [
              "right frame overflow to next left frame",
              "yellow box bottom",
              "green vertical line height"
            ]
          }
        },
        {
          "id": "part2_rows_01_08",
          "type": "vocabularyFixedRows",
          "titleLayerPolicy": "preserveTemplateTitleLayer",
          "rowHeightPolicy": "fixedFromTemplate",
          "overflowPolicy": "wrapInsideFixedTextBoxOrFlagReview",
          "rows": [
            {
              "rowNo": 1,
              "fixedHeight": true,
              "group": "@PART2_VOCAB_ROW_01_GROUP",
              "slots": {
                "no": {
                  "top": 1943,
                  "left": 2853,
                  "bottom": 1987,
                  "right": 2895
                },
                "word": {
                  "top": 1939,
                  "left": 2921,
                  "bottom": 1988,
                  "right": 3132
                },
                "phonetic": {
                  "top": 1905,
                  "left": 3402,
                  "bottom": 2038,
                  "right": 3736
                },
                "meaning": {
                  "top": 1938,
                  "left": 4062,
                  "bottom": 2003,
                  "right": 4752
                }
              }
            },
            {
              "rowNo": 2,
              "fixedHeight": true,
              "group": "@PART2_VOCAB_ROW_02_GROUP",
              "slots": {
                "no": {
                  "top": 2121,
                  "left": 2850,
                  "bottom": 2167,
                  "right": 2895
                },
                "word": {
                  "top": 2119,
                  "left": 2922,
                  "bottom": 2167,
                  "right": 3400
                },
                "phonetic": {
                  "top": 2088,
                  "left": 3446,
                  "bottom": 2221,
                  "right": 4039
                },
                "meaning": {
                  "top": 2111,
                  "left": 4106,
                  "bottom": 2166,
                  "right": 4278
                }
              }
            },
            {
              "rowNo": 3,
              "fixedHeight": true,
              "group": "@PART2_VOCAB_ROW_03_GROUP",
              "slots": {
                "no": {
                  "top": 2300,
                  "left": 2850,
                  "bottom": 2346,
                  "right": 2895
                },
                "word": {
                  "top": 2298,
                  "left": 2924,
                  "bottom": 2358,
                  "right": 3141
                },
                "phonetic": {
                  "top": 2265,
                  "left": 3402,
                  "bottom": 2402,
                  "right": 3776
                },
                "meaning": {
                  "top": 2297,
                  "left": 4063,
                  "bottom": 2357,
                  "right": 4405
                }
              }
            },
            {
              "rowNo": 4,
              "fixedHeight": true,
              "group": "@PART2_VOCAB_ROW_04_GROUP",
              "slots": {
                "no": {
                  "top": 2480,
                  "left": 2849,
                  "bottom": 2525,
                  "right": 2895
                },
                "word": {
                  "top": 2477,
                  "left": 2922,
                  "bottom": 2538,
                  "right": 3196
                },
                "phonetic": {
                  "top": 2446,
                  "left": 3402,
                  "bottom": 2583,
                  "right": 3729
                },
                "meaning": {
                  "top": 2469,
                  "left": 4062,
                  "bottom": 2529,
                  "right": 4507
                }
              }
            },
            {
              "rowNo": 5,
              "fixedHeight": true,
              "group": "@PART2_VOCAB_ROW_05_GROUP",
              "slots": {
                "no": {
                  "top": 2661,
                  "left": 2850,
                  "bottom": 2706,
                  "right": 2895
                },
                "word": {
                  "top": 2658,
                  "left": 2919,
                  "bottom": 2706,
                  "right": 3106
                },
                "phonetic": {
                  "top": 2625,
                  "left": 3402,
                  "bottom": 2757,
                  "right": 3691
                },
                "meaning": {
                  "top": 2657,
                  "left": 4063,
                  "bottom": 2713,
                  "right": 4638
                }
              }
            },
            {
              "rowNo": 6,
              "fixedHeight": true,
              "group": "@PART2_VOCAB_ROW_06_GROUP",
              "slots": {
                "no": {
                  "top": 2839,
                  "left": 2851,
                  "bottom": 2885,
                  "right": 2895
                },
                "word": {
                  "top": 2840,
                  "left": 2925,
                  "bottom": 2885,
                  "right": 3110
                },
                "phonetic": {
                  "top": 2806,
                  "left": 3402,
                  "bottom": 2943,
                  "right": 3786
                },
                "meaning": {
                  "top": 2829,
                  "left": 4063,
                  "bottom": 2885,
                  "right": 4697
                }
              }
            },
            {
              "rowNo": 7,
              "fixedHeight": true,
              "group": "@PART2_VOCAB_ROW_07_GROUP",
              "slots": {
                "no": {
                  "top": 3019,
                  "left": 2851,
                  "bottom": 3064,
                  "right": 2895
                },
                "word": {
                  "top": 3016,
                  "left": 2924,
                  "bottom": 3076,
                  "right": 3203
                },
                "phonetic": {
                  "top": 2983,
                  "left": 3402,
                  "bottom": 3120,
                  "right": 3807
                },
                "meaning": {
                  "top": 3015,
                  "left": 4063,
                  "bottom": 3075,
                  "right": 4503
                }
              }
            },
            {
              "rowNo": 8,
              "fixedHeight": true,
              "group": "@PART2_VOCAB_ROW_08_GROUP",
              "slots": {
                "no": {
                  "top": 3197,
                  "left": 2851,
                  "bottom": 3243,
                  "right": 2895
                },
                "word": {
                  "top": 3195,
                  "left": 2922,
                  "bottom": 3243,
                  "right": 3152
                },
                "phonetic": {
                  "top": 3164,
                  "left": 3402,
                  "bottom": 3296,
                  "right": 3754
                },
                "meaning": {
                  "top": 3187,
                  "left": 4062,
                  "bottom": 3251,
                  "right": 4348
                }
              }
            }
          ],
          "items": [
            {
              "no": "1",
              "word": "international",
              "kk": "KK: [ˌɪntɚˈnæʃənl]",
              "ipa": "IPA: [ˌɪntərˈnæʃənəl]",
              "meaning": "adj. 国际性的；国际间的",
              "raw": "international KK: [ˌɪntɚˈnæʃənl] IPA: [ˌɪntərˈnæʃənəl] adj. 国际性的；国际间的"
            },
            {
              "no": "2",
              "word": "language",
              "kk": "KK: [ˈlæŋɡwɪdʒ]",
              "ipa": "IPA: [ˈlæŋɡwɪdʒ]",
              "meaning": "n. 语言（可数）；言词（不可数）",
              "raw": "language KK: [ˈlæŋɡwɪdʒ] IPA: [ˈlæŋɡwɪdʒ] n. 语言（可数）；言词（不可数）"
            },
            {
              "no": "3",
              "word": "rewarding",
              "kk": "KK: [rɪˈwɔrdɪŋ]",
              "ipa": "IPA: [rɪˈwɔːrdɪŋ]",
              "meaning": "adj. 有（获）益的；值得做的；划算的",
              "raw": "rewarding KK: [rɪˈwɔrdɪŋ] IPA: [rɪˈwɔːrdɪŋ] adj. 有（获）益的；值得做的；划算的"
            },
            {
              "no": "4",
              "word": "depend on",
              "kk": "KK: [dɪˈpɛnd ɑn]",
              "ipa": "IPA: [dɪˈpend ɑːn]",
              "meaning": "视……而定",
              "raw": "depend on KK: [dɪˈpɛnd ɑn] IPA: [dɪˈpend ɑːn] 视……而定"
            },
            {
              "no": "5",
              "word": "tip",
              "kk": "KK: [tɪp]",
              "ipa": "IPA: [tɪp]",
              "meaning": "n. 建议；小费",
              "raw": "tip KK: [tɪp] IPA: [tɪp] n. 建议；小费"
            },
            {
              "no": "6",
              "word": "afraid",
              "kk": "KK: [əˈfred]",
              "ipa": "IPA: [əˈfreɪd]",
              "meaning": "adj. 害怕的；恐惧的",
              "raw": "afraid KK: [əˈfred] IPA: [əˈfreɪd] adj. 害怕的；恐惧的"
            },
            {
              "no": "7",
              "word": "be afraid to +动词原形",
              "kk": "KK: [bi əˈfred tu]",
              "ipa": "IPA: [bi əˈfreɪd tu]",
              "meaning": "害怕去做……",
              "raw": "be afraid to +动词原形 KK: [bi əˈfred tu] IPA: [bi əˈfreɪd tu] 害怕去做……"
            },
            {
              "no": "8",
              "word": "shy",
              "kk": "KK: [ʃaɪ]",
              "ipa": "IPA: [ʃaɪ]",
              "meaning": "adj. 羞怯的",
              "raw": "shy KK: [ʃaɪ] IPA: [ʃaɪ] adj. 羞怯的"
            }
          ]
        }
      ]
    },
    {
      "pageIndex": 2,
      "template": "3-4 2.psd",
      "pageNumbers": [
        "003",
        "004"
      ],
      "frames": {
        "left": {
          "top": 421,
          "left": 200,
          "bottom": 3311,
          "right": 2149
        },
        "right": {
          "top": 421,
          "left": 2773,
          "bottom": 3311,
          "right": 4840
        },
        "source": "hidden PSD reference layers; keep hidden in output"
      },
      "hiddenLayers": [
        "@SHELL_CONTENT_PANEL_DECOR_SHAPE",
        "@SHELL_CONTENT_PANEL_LEFT",
        "@SHELL_CONTENT_PANEL_RIGHT",
        "@SHELL_PANEL_CORNER_DECOR_RIGHT",
        "@SHELL_PANEL_CORNER_DECOR_LEFT"
      ],
      "modules": [
        {
          "id": "part2_rows_09_21",
          "type": "vocabularyFixedRows",
          "rowHeightPolicy": "fixedFromTemplate",
          "overflowPolicy": "wrapInsideFixedTextBoxOrFlagReview",
          "rows": [
            {
              "rowNo": 9,
              "fixedHeight": true,
              "group": "@PART2_VOCAB_ROW_09_GROUP",
              "slots": {
                "no": {
                  "top": 485,
                  "left": 311,
                  "bottom": 530,
                  "right": 356
                },
                "word": {
                  "top": 483,
                  "left": 381,
                  "bottom": 531,
                  "right": 529
                },
                "phonetic": {
                  "top": 447,
                  "left": 834,
                  "bottom": 578,
                  "right": 1121
                },
                "meaning": {
                  "top": 481,
                  "left": 1381,
                  "bottom": 542,
                  "right": 1992
                }
              }
            },
            {
              "rowNo": 10,
              "fixedHeight": true,
              "group": "@PART2_VOCAB_ROW_10_GROUP",
              "slots": {
                "no": {
                  "top": 664,
                  "left": 282,
                  "bottom": 709,
                  "right": 357
                },
                "word": {
                  "top": 661,
                  "left": 381,
                  "bottom": 710,
                  "right": 646
                },
                "phonetic": {
                  "top": 632,
                  "left": 834,
                  "bottom": 763,
                  "right": 1177
                },
                "meaning": {
                  "top": 654,
                  "left": 1379,
                  "bottom": 709,
                  "right": 1665
                }
              }
            },
            {
              "rowNo": 11,
              "fixedHeight": true,
              "group": "@PART2_VOCAB_ROW_11_GROUP",
              "slots": {
                "no": {
                  "top": 846,
                  "left": 282,
                  "bottom": 890,
                  "right": 357
                },
                "word": {
                  "top": 849,
                  "left": 382,
                  "bottom": 891,
                  "right": 588
                },
                "phonetic": {
                  "top": 809,
                  "left": 834,
                  "bottom": 942,
                  "right": 1189
                },
                "meaning": {
                  "top": 842,
                  "left": 1381,
                  "bottom": 902,
                  "right": 1820
                }
              }
            },
            {
              "rowNo": 12,
              "fixedHeight": true,
              "group": "@PART2_VOCAB_ROW_12_GROUP",
              "slots": {
                "no": {
                  "top": 1024,
                  "left": 280,
                  "bottom": 1069,
                  "right": 355
                },
                "word": {
                  "top": 1022,
                  "left": 382,
                  "bottom": 1083,
                  "right": 566
                },
                "phonetic": {
                  "top": 993,
                  "left": 834,
                  "bottom": 1128,
                  "right": 1137
                },
                "meaning": {
                  "top": 1013,
                  "left": 1381,
                  "bottom": 1070,
                  "right": 1989
                }
              }
            },
            {
              "rowNo": 13,
              "fixedHeight": true,
              "group": "@PART2_VOCAB_ROW_13_GROUP",
              "slots": {
                "no": {
                  "top": 1203,
                  "left": 282,
                  "bottom": 1248,
                  "right": 357
                },
                "word": {
                  "top": 1200,
                  "left": 381,
                  "bottom": 1249,
                  "right": 585
                },
                "phonetic": {
                  "top": 1168,
                  "left": 834,
                  "bottom": 1301,
                  "right": 1149
                },
                "meaning": {
                  "top": 1200,
                  "left": 1379,
                  "bottom": 1264,
                  "right": 1869
                }
              }
            },
            {
              "rowNo": 14,
              "fixedHeight": true,
              "group": "@PART2_VOCAB_ROW_14_GROUP",
              "slots": {
                "no": {
                  "top": 1383,
                  "left": 281,
                  "bottom": 1427,
                  "right": 356
                },
                "word": {
                  "top": 1380,
                  "left": 382,
                  "bottom": 1428,
                  "right": 523
                },
                "phonetic": {
                  "top": 1350,
                  "left": 834,
                  "bottom": 1481,
                  "right": 1115
                },
                "meaning": {
                  "top": 1372,
                  "left": 1381,
                  "bottom": 1427,
                  "right": 1613
                }
              }
            },
            {
              "rowNo": 15,
              "fixedHeight": true,
              "group": "@PART2_VOCAB_ROW_15_GROUP",
              "slots": {
                "no": {
                  "top": 1564,
                  "left": 282,
                  "bottom": 1608,
                  "right": 357
                },
                "word": {
                  "top": 1561,
                  "left": 379,
                  "bottom": 1609,
                  "right": 571
                },
                "phonetic": {
                  "top": 1527,
                  "left": 834,
                  "bottom": 1660,
                  "right": 1141
                },
                "meaning": {
                  "top": 1560,
                  "left": 1381,
                  "bottom": 1615,
                  "right": 1613
                }
              }
            },
            {
              "rowNo": 16,
              "fixedHeight": true,
              "group": "@PART2_VOCAB_ROW_16_GROUP",
              "slots": {
                "no": {
                  "top": 1743,
                  "left": 282,
                  "bottom": 1789,
                  "right": 357
                },
                "word": {
                  "top": 1741,
                  "left": 385,
                  "bottom": 1789,
                  "right": 728
                },
                "phonetic": {
                  "top": 1708,
                  "left": 834,
                  "bottom": 1840,
                  "right": 1263
                },
                "meaning": {
                  "top": 1740,
                  "left": 1379,
                  "bottom": 1795,
                  "right": 1490
                }
              }
            },
            {
              "rowNo": 17,
              "fixedHeight": true,
              "group": "@PART2_VOCAB_ROW_17_GROUP",
              "slots": {
                "no": {
                  "top": 1923,
                  "left": 282,
                  "bottom": 1968,
                  "right": 357
                },
                "word": {
                  "top": 1920,
                  "left": 385,
                  "bottom": 1968,
                  "right": 601
                },
                "phonetic": {
                  "top": 1889,
                  "left": 834,
                  "bottom": 2026,
                  "right": 1197
                },
                "meaning": {
                  "top": 1912,
                  "left": 1377,
                  "bottom": 1972,
                  "right": 1716
                }
              }
            },
            {
              "rowNo": 18,
              "fixedHeight": true,
              "group": "@PART2_VOCAB_ROW_18_GROUP",
              "slots": {
                "no": {
                  "top": 2103,
                  "left": 282,
                  "bottom": 2149,
                  "right": 357
                },
                "word": {
                  "top": 2067,
                  "left": 382,
                  "bottom": 2190,
                  "right": 758
                },
                "phonetic": {
                  "top": 2069,
                  "left": 834,
                  "bottom": 2200,
                  "right": 1572
                },
                "meaning": {
                  "top": 2065,
                  "left": 1634,
                  "bottom": 2207,
                  "right": 2035
                }
              }
            },
            {
              "rowNo": 19,
              "fixedHeight": true,
              "group": "@PART2_VOCAB_ROW_19_GROUP",
              "slots": {
                "no": {
                  "top": 2282,
                  "left": 280,
                  "bottom": 2328,
                  "right": 355
                },
                "word": {
                  "top": 2279,
                  "left": 382,
                  "bottom": 2328,
                  "right": 619
                },
                "phonetic": {
                  "top": 2249,
                  "left": 834,
                  "bottom": 2382,
                  "right": 1230
                },
                "meaning": {
                  "top": 2272,
                  "left": 1379,
                  "bottom": 2336,
                  "right": 2070
                }
              }
            },
            {
              "rowNo": 20,
              "fixedHeight": true,
              "group": "@PART2_VOCAB_ROW_20_GROUP",
              "slots": {
                "no": {
                  "top": 2461,
                  "left": 279,
                  "bottom": 2507,
                  "right": 357
                },
                "word": {
                  "top": 2459,
                  "left": 385,
                  "bottom": 2507,
                  "right": 496
                },
                "phonetic": {
                  "top": 2428,
                  "left": 834,
                  "bottom": 2559,
                  "right": 1081
                },
                "meaning": {
                  "top": 2458,
                  "left": 1377,
                  "bottom": 2513,
                  "right": 1699
                }
              }
            },
            {
              "rowNo": 21,
              "fixedHeight": true,
              "group": "@PART2_VOCAB_ROW_21_GROUP",
              "slots": {
                "no": {
                  "top": 2640,
                  "left": 278,
                  "bottom": 2686,
                  "right": 356
                },
                "word": {
                  "top": 2638,
                  "left": 385,
                  "bottom": 2686,
                  "right": 519
                },
                "phonetic": {
                  "top": 2608,
                  "left": 834,
                  "bottom": 2744,
                  "right": 1110
                },
                "meaning": {
                  "top": 2631,
                  "left": 1381,
                  "bottom": 2690,
                  "right": 1716
                }
              }
            }
          ],
          "items": [
            {
              "no": "9",
              "word": "thick-skinned",
              "kk": "KK: [ˌθɪkˈskɪnd]",
              "ipa": "IPA: [ˌθɪkˈskɪnd]",
              "meaning": "adj. 厚脸皮的",
              "raw": "thick-skinned KK: [ˌθɪkˈskɪnd] IPA: [ˌθɪkˈskɪnd] adj. 厚脸皮的"
            },
            {
              "no": "10",
              "word": "speak up",
              "kk": "KK: [spik ʌp]",
              "ipa": "IPA: [spiːk ʌp]",
              "meaning": "大声说话；开口说出来",
              "raw": "speak up KK: [spik ʌp] IPA: [spiːk ʌp] 大声说话；开口说出来"
            },
            {
              "no": "11",
              "word": "patient",
              "kk": "KK: [ˈpeʃənt]",
              "ipa": "IPA: [ˈpeɪʃənt]",
              "meaning": "adj. 有耐心的（常与介词 with连用）",
              "raw": "patient KK: [ˈpeʃənt] IPA: [ˈpeɪʃənt] adj. 有耐心的（常与介词 with连用）"
            },
            {
              "no": "12",
              "word": "improve",
              "kk": "KK: [ɪmˈpruv]",
              "ipa": "IPA: [ɪmˈpruːv]",
              "meaning": "vt. & vi.（使）进步；改善",
              "raw": "improve KK: [ɪmˈpruv] IPA: [ɪmˈpruːv] vt. & vi.（使）进步；改善"
            },
            {
              "no": "13",
              "word": "hi",
              "kk": "KK: [haɪ]",
              "ipa": "IPA: [haɪ]",
              "meaning": "int. 嗨（打招呼声）",
              "raw": "hi KK: [haɪ] IPA: [haɪ] int. 嗨（打招呼声）"
            },
            {
              "no": "14",
              "word": "kid",
              "kk": "KK: [kɪd]",
              "ipa": "IPA: [kɪd]",
              "meaning": "vt. & vi.（口语）（与……）开玩笑 & n. 小孩",
              "raw": "kid KK: [kɪd] IPA: [kɪd] vt. & vi.（口语）（与……）开玩笑 & n. 小孩"
            }
          ],
          "emptyRowsPolicy": "hideUnusedRows"
        },
        {
          "id": "part3_start",
          "type": "grammarFlow",
          "titleLayerPolicy": "preserveTemplateTitleLayer",
          "lead": "本节课主要学习特殊疑问词引导的名词性从句。",
          "sections": [
            {
              "title": null,
              "blocks": [
                {
                  "type": "paragraph",
                  "text": "对于特殊疑问句，我们只需要把特殊疑问词后面倒装的句子还原成正常的语序就可以当名词性从句用了，比如：",
                  "runs": [
                    {
                      "text": "对于特殊疑问句，我们只需要把特殊疑问词后面倒装的句子还原成正常的语序就可以当名词性从句用了，比如：",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    }
                  ]
                },
                {
                  "type": "transformExample",
                  "text": "What is your name? 变从句 → what your name is. be动词回到主语后面",
                  "runs": [
                    {
                      "text": "    ",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "What is your name?  ",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "变从句",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "  ",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "→",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": " what your name is.   ",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "be",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "动词回到主语后面",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    }
                  ]
                },
                {
                  "type": "transformExample",
                  "text": "Where will Vicky go? 变从句 → where Vicky will go. 助动词（can，will，have等）回到主语后面，这类助动词要么本身是情态动词，有确切的意思，修饰谓语动词，要么是为了帮助构成时态，变回陈述句语序后，其意思和时态都不变，因此仍然需要这些词，不能省掉。",
                  "runs": [
                    {
                      "text": "    Where will Vicky go?  ",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "变从句",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "  ",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "→",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": " where Vicky will go.   ",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "助动词",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "（",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "can",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "，",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "will",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "，",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "have",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "等",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "）",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "回到主语后面，这类助动词要么本身是情态动词，有确切的意思，修饰谓语动词，要么是为了帮助构成时态，变回陈述句语序后，其意思和时态都不变，因此仍然需要这些词，不能省掉。",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    }
                  ]
                },
                {
                  "type": "transformExample",
                  "text": "Why does Vicky like kids? 变从句 → why Vicky likes kids. 助动词（do，does，did等）去除，动词还原成应有的时态，这里为一般现在时，所以动词要用三单。这类助动词只是为了帮助构成特殊疑问句，变从句后原来的句子还原成陈述句语序了，不再是特殊疑问句了，所以要将助动词去掉。",
                  "runs": [
                    {
                      "text": "    ",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "Why does Vicky like kids?  ",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "变从句",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "  ",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "→",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": " why Vicky likes kids.   ",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "助动词",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "（",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "do",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "，",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "does",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "，",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "did",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "等",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "）",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "去除，动词还原成应有的时态，这里为一般",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "现在",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "时，所以动词要用三单。这类助动词只是为了帮助构成特殊疑问句，变从句后原来的句子还原成陈述句语序了，不再是特殊疑问句了，所以要将助动词去掉。",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    }
                  ]
                },
                {
                  "type": "paragraph",
                  "text": "例子：",
                  "runs": [
                    {
                      "text": "    ",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "例子",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "：",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    }
                  ]
                },
                {
                  "type": "numberedExample",
                  "text": "①What your name is doesn't matter to me. 名词性从句作主语",
                  "runs": [
                    {
                      "text": "①",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "What your name is doesn",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "’",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "t matter to me.    ",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "名词性从句作主语",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    }
                  ]
                },
                {
                  "type": "numberedExample",
                  "text": "②The question is where Vicky will go. 名词性从句作表语",
                  "runs": [
                    {
                      "text": "②",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "The question is where Vicky will go.    ",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "名词性从句作表语",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    }
                  ]
                },
                {
                  "type": "numberedExample",
                  "text": "③I don't know why Vicky likes kids. 名词性从句作动词的宾语",
                  "runs": [
                    {
                      "text": "③",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "I don",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "’",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "t know why Vicky likes kids.    ",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "名词性从句作动词的宾语",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    }
                  ]
                },
                {
                  "type": "numberedExample",
                  "text": "④We are talking about where Vicky will go. 名词性从句作介词的宾语",
                  "runs": [
                    {
                      "text": "④",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "We are talking about where Vicky will go. ",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    },
                    {
                      "text": "名词性从句作介词的宾语",
                      "color": null,
                      "highlight": null,
                      "italic": false,
                      "bold": false
                    }
                  ]
                }
              ]
            }
          ],
          "subtitlePolicy": "hideSubtitleGroupsWhenWordHasNoSectionTitle"
        }
      ]
    },
    {
      "pageIndex": 3,
      "template": "3-4 3.psd",
      "pageNumbers": [
        "005",
        "006"
      ],
      "frames": {
        "left": {
          "top": 418,
          "left": 200,
          "bottom": 3308,
          "right": 2149
        },
        "right": {
          "top": 418,
          "left": 2773,
          "bottom": 3308,
          "right": 4840
        },
        "source": "hidden PSD reference layers; keep hidden in output"
      },
      "hiddenLayers": [
        "@SHELL_CONTENT_PANEL_DECOR_SHAPE",
        "@SHELL_CONTENT_PANEL_LEFT",
        "@SHELL_CONTENT_PANEL_RIGHT",
        "@SHELL_PANEL_CORNER_DECOR_RIGHT",
        "@SHELL_PANEL_CORNER_DECOR_LEFT"
      ],
      "modules": [
        {
          "id": "part3_cont",
          "type": "grammarFlowContinuation",
          "source": "part3_start"
        }
      ]
    },
    {
      "pageIndex": 4,
      "template": "3-4 4.psd",
      "pageNumbers": [
        "007",
        "008"
      ],
      "frames": {
        "left": {
          "top": 421,
          "left": 200,
          "bottom": 3311,
          "right": 2149
        },
        "right": {
          "top": 421,
          "left": 2773,
          "bottom": 3311,
          "right": 4840
        },
        "source": "hidden PSD reference layers; keep hidden in output"
      },
      "hiddenLayers": [
        "@SHELL_CONTENT_PANEL_DECOR_SHAPE",
        "@SHELL_CONTENT_PANEL_LEFT",
        "@SHELL_CONTENT_PANEL_RIGHT",
        "@SHELL_PANEL_CORNER_DECOR_RIGHT",
        "@SHELL_PANEL_CORNER_DECOR_LEFT"
      ],
      "modules": [
        {
          "id": "part3_end",
          "type": "grammarFlowContinuation",
          "source": "part3_start"
        },
        {
          "id": "part4_start",
          "type": "exerciseFlow",
          "titleLayerPolicy": "showOnceAtExerciseStart",
          "blocks": [
            {
              "kind": "sectionTitle",
              "sectionNo": "1.",
              "text": "从下列句子中找出名词性从句，在从句下方画横线。"
            },
            {
              "kind": "exerciseItem",
              "itemNo": "①",
              "text": "① What he needs is more time.",
              "answerLines": 0,
              "keepTogether": true
            },
            {
              "kind": "exerciseItem",
              "itemNo": "②",
              "text": "② What you learn will help you later.",
              "answerLines": 0,
              "keepTogether": true
            },
            {
              "kind": "exerciseItem",
              "itemNo": "③",
              "text": "③ This is what I have been looking for.",
              "answerLines": 0,
              "keepTogether": true
            },
            {
              "kind": "exerciseItem",
              "itemNo": "④",
              "text": "④ Life is what you make it.",
              "answerLines": 0,
              "keepTogether": true
            },
            {
              "kind": "exerciseItem",
              "itemNo": "⑤",
              "text": "⑤ I can't remember what she told me.",
              "answerLines": 0,
              "keepTogether": true
            },
            {
              "kind": "exerciseItem",
              "itemNo": "⑥",
              "text": "⑥ He didn't understand what I meant.",
              "answerLines": 0,
              "keepTogether": true
            },
            {
              "kind": "exerciseItem",
              "itemNo": "⑦",
              "text": "⑦ She finally realized what her mistake was.",
              "answerLines": 0,
              "keepTogether": true
            },
            {
              "kind": "exerciseItem",
              "itemNo": "⑧",
              "text": "⑧ We are worried about what will happen next.",
              "answerLines": 0,
              "keepTogether": true
            },
            {
              "kind": "exerciseItem",
              "itemNo": "⑨",
              "text": "⑨ She cares about what others think of her.",
              "answerLines": 0,
              "keepTogether": true
            },
            {
              "kind": "exerciseItem",
              "itemNo": "⑩",
              "text": "⑩ They are talking about what happened yesterday.",
              "answerLines": 0,
              "keepTogether": true
            },
            {
              "kind": "sectionTitle",
              "sectionNo": "2.",
              "text": "翻译"
            },
            {
              "kind": "exerciseItem",
              "itemNo": "①",
              "text": "① 我不知道如何提高我的国际语言水平。（international language）",
              "answerLines": 1,
              "keepTogether": true
            },
            {
              "kind": "exerciseItem",
              "itemNo": "②",
              "text": "② 他告诉我的是一些很有用的建议。（useful）",
              "answerLines": 1,
              "keepTogether": true
            },
            {
              "kind": "exerciseItem",
              "itemNo": "③",
              "text": "③ 问题是我们为什么要学得脸皮厚一点。（problem; thick-skinned）",
              "answerLines": 1,
              "keepTogether": true
            },
            {
              "kind": "exerciseItem",
              "itemNo": "④",
              "text": "④ 我明白了什么才是真正值得做的事。（worthy）",
              "answerLines": 1,
              "keepTogether": true
            },
            {
              "kind": "exerciseItem",
              "itemNo": "⑤",
              "text": "⑤ 她害怕别人会怎么看她。（be afraid to）",
              "answerLines": 1,
              "keepTogether": true
            },
            {
              "kind": "exerciseItem",
              "itemNo": "⑥",
              "text": "⑥ 他在问我这些语言技巧来自哪里。（language skills）",
              "answerLines": 1,
              "keepTogether": true
            },
            {
              "kind": "exerciseItem",
              "itemNo": "⑦",
              "text": "⑦ 成功的关键是你是否愿意不断进步。（success; key; improve）",
              "answerLines": 1,
              "keepTogether": true
            },
            {
              "kind": "exerciseItem",
              "itemNo": "⑧",
              "text": "⑧ 我们正在讨论怎样学习国际语言才更有效。（effectively）",
              "answerLines": 1,
              "keepTogether": true
            },
            {
              "kind": "exerciseItem",
              "itemNo": "⑨",
              "text": "⑨ 他只是在开玩笑，这就是我想说的。（kid）",
              "answerLines": 1,
              "keepTogether": true
            },
            {
              "kind": "exerciseItem",
              "itemNo": "⑩",
              "text": "⑩ 你有多耐心决定了你能进步多快。（patient; decide; improve）",
              "answerLines": 1,
              "keepTogether": true
            }
          ],
          "keepTogetherPolicy": "exerciseItemAndAnswerLines"
        }
      ]
    },
    {
      "pageIndex": 5,
      "template": "3-4 5.psd",
      "pageNumbers": [
        "009",
        "010"
      ],
      "frames": {
        "left": {
          "top": 421,
          "left": 200,
          "bottom": 3311,
          "right": 2149
        },
        "right": {
          "top": 421,
          "left": 2773,
          "bottom": 3311,
          "right": 4840
        },
        "source": "hidden PSD reference layers; keep hidden in output"
      },
      "hiddenLayers": [
        "@SHELL_CONTENT_PANEL_DECOR_SHAPE",
        "@SHELL_CONTENT_PANEL_LEFT",
        "@SHELL_CONTENT_PANEL_RIGHT",
        "@SHELL_PANEL_CORNER_DECOR_RIGHT",
        "@SHELL_PANEL_CORNER_DECOR_LEFT"
      ],
      "modules": [
        {
          "id": "part4_cont",
          "type": "exerciseFlowContinuation",
          "source": "part4_start"
        }
      ]
    }
  ],
  "unresolvedRequiresPhotoshopMeasurement": [
    "exact text wrap using PSD font metrics",
    "Part1 reading green border dynamic resize",
    "Dialogue yellow box and green line dynamic resize",
    "flow break positions after actual Photoshop text composition"
  ]
};
var layerMap = {};
var logFile = null;

function ensureFolder(path) {
  var folder = new Folder(path);
  if (!folder.exists) folder.create();
}

function walkLayers(container, callback) {
  for (var i = 0; i < container.layers.length; i++) {
    var layer = container.layers[i];
    callback(layer);
    if (layer.typename === "LayerSet") walkLayers(layer, callback);
  }
}

var TRACE = [];

function openLog() {
  logFile = new File(OUT + "/layout_log.txt");
  logFile.encoding = "UTF-8";
  logFile.open("w");
  log("START lessonIndex=" + START_LESSON_INDEX + "-" + END_LESSON_INDEX + " lesson=" + DATA.lessonNo);
}

function log(message) {
  if (logFile) logFile.writeln(new Date().toISOString ? new Date().toISOString() + "\t" + message : message);
}

function closeLog() {
  if (logFile) {
    log("END");
    logFile.close();
    logFile = null;
  }
}

function unlockLayer(layer) {
  try { layer.allLocked = false; } catch (e) {}
  try { layer.pixelsLocked = false; } catch (e) {}
  try { layer.positionLocked = false; } catch (e) {}
  try { layer.transparentPixelsLocked = false; } catch (e) {}
}

function unlockAll(doc) {
  walkLayers(doc, function(layer) {
    unlockLayer(layer);
  });
}

function buildLayerMap(doc) {
  layerMap = {};
  walkLayers(doc, function(layer) {
    if (!layerMap[layer.name]) layerMap[layer.name] = layer;
  });
}

function findLayer(doc, name) {
  return layerMap[name] || null;
}

function setText(doc, name, value) {
  var layer = findLayer(doc, name);
  if (!layer) {
    TRACE.push("MISSING " + name);
    log("MISSING_LAYER " + name);
    return false;
  }
  layer.visible = true;
  unlockLayer(layer);
  if (layer.kind === LayerKind.TEXT) {
    try {
      doc.activeLayer = layer;
      layer.textItem.contents = value || "";
      log("SET_TEXT " + name);
    } catch (e) {
      TRACE.push("SET_TEXT_FAILED " + name + " :: " + e.message);
      log("SET_TEXT_FAILED " + name + " :: " + e.message);
      return false;
    }
  }
  return true;
}

function moveLayerTopLeft(layer, targetLeft, targetTop) {
  if (!layer) return;
  try {
    var b = layer.bounds;
    var left = b[0].as("px");
    var top = b[1].as("px");
    layer.translate(UnitValue(targetLeft - left, "px"), UnitValue(targetTop - top, "px"));
  } catch (e) {
    TRACE.push("MOVE_FAILED " + layer.name + " :: " + e.message);
  }
}

function bringLayerToDocumentTop(doc, layer) {
  if (!layer || doc.layers.length < 1) return;
  try {
    layer.move(doc.layers[0], ElementPlacement.PLACEBEFORE);
  } catch (e) {
    TRACE.push("BRING_TO_TOP_FAILED " + layer.name + " :: " + e.message);
  }
}

function requireStyleSource(doc, sourceName) {
  var source = findLayer(doc, sourceName);
  if (!source) {
    TRACE.push("MISSING_STYLE_SOURCE " + sourceName);
    log("MISSING_STYLE_SOURCE " + sourceName);
    throw new Error("Missing PSD style source: " + sourceName);
  }
  if (source.kind !== LayerKind.TEXT) {
    TRACE.push("INVALID_STYLE_SOURCE " + sourceName);
    log("INVALID_STYLE_SOURCE " + sourceName);
    throw new Error("PSD style source is not a text layer: " + sourceName);
  }
  return source;
}

function duplicateTextLayer(doc, sourceName, newName, text, targetLeft, targetTop) {
  var source = requireStyleSource(doc, sourceName);
  var layer = source.duplicate();
  layer.name = newName;
  unlockLayer(layer);
  layer.visible = true;
  if (layer.kind === LayerKind.TEXT) {
    doc.activeLayer = layer;
    layer.textItem.contents = text || "";
  }
  moveLayerTopLeft(layer, targetLeft, targetTop);
  bringLayerToDocumentTop(doc, layer);
  layerMap[newName] = layer;
  log("CREATE_TEXT " + newName + " styleSource=" + sourceName);
  return layer;
}

function measureTextRight(doc, sourceName, text, targetLeft, targetTop) {
  var layer = duplicateTextLayer(doc, sourceName, "@RUN_MEASURE_TEXT_TMP", text, targetLeft, targetTop);
  if (!layer) return targetLeft;
  var right = targetLeft;
  try {
    var b = layer.bounds;
    right = b[2].as("px");
  } catch (e) {
    TRACE.push("MEASURE_TEXT_RIGHT_FAILED :: " + e.message);
  }
  try { layer.remove(); } catch (e2) {}
  layerMap["@RUN_MEASURE_TEXT_TMP"] = null;
  return right;
}

function splitTextByMeasuredRight(doc, sourceName, text, targetLeft, targetTop, maxRight) {
  var words = (text || "").split(/\s+/);
  var lines = [];
  var current = "";
  for (var i = 0; i < words.length; i++) {
    if (!words[i]) continue;
    var candidate = current ? current + " " + words[i] : words[i];
    if (current && measureTextRight(doc, sourceName, candidate, targetLeft, targetTop) > maxRight) {
      lines.push(current);
      current = words[i];
    } else {
      current = candidate;
    }
  }
  if (current) lines.push(current);
  return lines;
}

function applyFontFromStyleSource(doc, targetName, sourceName) {
  var target = findLayer(doc, targetName);
  var source = requireStyleSource(doc, sourceName);
  if (!target || target.kind !== LayerKind.TEXT) {
    TRACE.push("MISSING_TEXT_FOR_STYLE " + targetName);
    log("MISSING_TEXT_FOR_STYLE " + targetName);
    return false;
  }
  try {
    target.textItem.font = source.textItem.font;
    log("APPLY_FONT_SOURCE target=" + targetName + " source=" + sourceName);
    return true;
  } catch (e) {
    TRACE.push("APPLY_FONT_SOURCE_FAILED " + targetName + " :: " + e.message);
    log("APPLY_FONT_SOURCE_FAILED " + targetName + " :: " + e.message);
    return false;
  }
}

function setOptionalText(doc, name, value) {
  var layer = findLayer(doc, name);
  if (!layer) return false;
  return setText(doc, name, value);
}

function hideLayer(doc, name) {
  var layer = findLayer(doc, name);
  if (layer) {
    layer.visible = false;
    log("HIDE_LAYER " + name);
  }
}

function setHeader(doc) {
  setText(doc, "@SHELL_TOP_LESSON_NO_TEXT", DATA.lessonNo);
  setText(doc, "@SHELL_TOP_LESSON_TITLE_TEXT", DATA.lessonTitle);
  setOptionalText(doc, "@LESSON_NO_COVER_TEXT", DATA.lessonNo);
  setOptionalText(doc, "@LESSON_TITLE_COVER_TEXT", DATA.lessonTitle);
}

function setPageNo(doc, left, right) {
  setText(doc, "@PAGE_NO_LEFT_TEXT", left);
  setText(doc, "@PAGE_NO_RIGHT_TEXT", right);
}

function applyHiddenLayers(doc, pageSpec) {
  var names = pageSpec.hiddenLayers || [];
  for (var i = 0; i < names.length; i++) {
    hideLayer(doc, names[i]);
  }
}

function hidePart3Subtitle(doc, no) {
  var id = no < 10 ? "0" + no : "" + no;
  hideLayer(doc, "@PART3_SUBTITLE_" + id + "_GROUP");
}

function hideAllPart3Subtitles(doc) {
  for (var i = 1; i <= 12; i++) {
    hidePart3Subtitle(doc, i);
  }
}

function applyPart3SubtitlePolicy(doc, pageSpec) {
  var modules = pageSpec.modules || [];
  for (var i = 0; i < modules.length; i++) {
    if ((modules[i].type === "grammarFlow" || modules[i].type === "grammarFlowContinuation") &&
        (modules[i].subtitlePolicy === "hideSubtitleGroupsWhenWordHasNoSectionTitle" || PLAN.rules.part3NoFakeSubtitles)) {
      hideAllPart3Subtitles(doc);
      return;
    }
  }
  if (PLAN.rules.part3NoFakeSubtitles) hideAllPart3Subtitles(doc);
}

function findModule(pageSpec, moduleId) {
  var modules = pageSpec.modules || [];
  for (var i = 0; i < modules.length; i++) {
    if (modules[i].id === moduleId) return modules[i];
  }
  throw new Error("Missing module " + moduleId + " on page " + pageSpec.pageIndex);
}

function fixedRowTextMayOverflow(text, limit) {
  return (text || "").length > limit;
}

function setVocabRowFromPlan(doc, rowSpec, item) {
  var rowNo = rowSpec.rowNo;
  var prefix = "@PART2_VOCAB_ROW_" + (rowNo < 10 ? "0" + rowNo : rowNo);
  if (!item) {
    hideLayer(doc, prefix + "_GROUP");
    setText(doc, prefix + "_NO_TEXT", "");
    setText(doc, prefix + "_WORD_TEXT", "");
    setText(doc, prefix + "_PHONETIC_TEXT", "");
    setText(doc, prefix + "_MEANING_TEXT", "");
    return;
  }
  setText(doc, prefix + "_NO_TEXT", item.no);
  setText(doc, prefix + "_WORD_TEXT", item.word);
  setText(doc, prefix + "_PHONETIC_TEXT", (item.kk || "") + (item.kk && item.ipa ? "\r" : "") + (item.ipa || ""));
  applyFontFromStyleSource(doc, prefix + "_PHONETIC_TEXT", "@PART1_READING_RIGHT_TEXT_STYLE_SOURCE");
  setText(doc, prefix + "_MEANING_TEXT", item.meaning);
  if (rowSpec.fixedHeight && (fixedRowTextMayOverflow(item.word, 32) || fixedRowTextMayOverflow(item.meaning, 42))) {
    TRACE.push("REVIEW_VOCAB_FIXED_BOX row=" + rowNo + " word=" + item.word);
  }
}

function applyVocabModule(doc, pageSpec, moduleId) {
  var module = findModule(pageSpec, moduleId);
  var rows = module.rows || [];
  var items = module.items || [];
  for (var i = 0; i < rows.length; i++) {
    setVocabRowFromPlan(doc, rows[i], items[i]);
  }
}

function applyPart1Module(doc, pageSpec) {
  var module = findModule(pageSpec, "part1");
  hideLayer(doc, "@PART1_READING_LEFT_TEXT_STYLE_SOURCE");
  hideLayer(doc, "@PART1_READING_RIGHT_TEXT_STYLE_SOURCE");
  layoutReadingLines(doc);
  setText(doc, "@PART1_DIALOGUE_INTRO_TEXT", DATA.dialogueIntro);
  setText(doc, "@PART1_DIALOGUE_ROLE_MAP_TEXT", DATA.dialogueRole);
  hideLayer(doc, "@PART1_DIALOGUE_SAMPLE_LINE_TEXT");
  layoutDialogueLines(doc);
  TRACE.push("MEASURE_REQUIRED part1 reading line wraps using PSD font metrics");
  TRACE.push("MEASURE_REQUIRED part1 reading green border bottom resize");
  TRACE.push("MEASURE_REQUIRED part1 dialogue yellow box bottom resize");
  TRACE.push("MEASURE_REQUIRED part1 dialogue green vertical line resize");
  TRACE.push("MEASURE_REQUIRED part1 dialogue overflow right frame to next left frame");
  if (module.dynamic !== true) TRACE.push("REVIEW part1 module is not marked dynamic");
}

function layoutReadingLines(doc) {
  var metrics = DATA.readingMetrics;
  var x = metrics.textX;
  var y = metrics.textTop;
  var maxRight = metrics.maxRight;
  var lineGap = metrics.lineGap;
  var firstLineX = x + (metrics.bodyFirstLineIndent || 0);
  var continuationX = x + (metrics.bodyContinuationIndent || 0);
  var blockLineCount = metrics.blockLineCount;
  var phoneticStyleSource = metrics.phoneticStyleSource;
  var bodyStyleSource = metrics.bodyStyleSource;
  requireStyleSource(doc, phoneticStyleSource);
  requireStyleSource(doc, bodyStyleSource);

  function lowerText(value) {
    return (value || "").toLowerCase();
  }

  function findTargetInLine(lineText, target) {
    if (!target) return -1;
    return lowerText(lineText).indexOf(lowerText(target));
  }

  function splitReadingBody(text, bodyTop) {
    var firstCandidates = splitTextByMeasuredRight(doc, bodyStyleSource, text, firstLineX, bodyTop, maxRight);
    var firstText = firstCandidates.length ? firstCandidates[0] : "";
    var remaining = "";
    if (firstText && text.length > firstText.length) {
      remaining = text.substring(firstText.length).replace(/^\s+/, "");
    }
    var lines = [];
    if (firstText) lines.push({ text: firstText, x: firstLineX, y: bodyTop });
    if (remaining) {
      var continuationLines = splitTextByMeasuredRight(doc, bodyStyleSource, remaining, continuationX, bodyTop + lineGap, maxRight);
      for (var c = 0; c < continuationLines.length; c++) {
        lines.push({ text: continuationLines[c], x: continuationX, y: bodyTop + lineGap * (c + 1) });
      }
    }
    return lines;
  }

  function placeReadingPhoneticSegments(block, bodyLines, phoneticTop, blockIndex) {
    var placed = 0;
    var segments = block.segments || [];
    for (var s = 0; s < segments.length; s++) {
      var segment = segments[s];
      var placedSegment = false;
      for (var l = 0; l < bodyLines.length; l++) {
        var line = bodyLines[l];
        var targetAt = findTargetInLine(line.text, segment.target);
        if (targetAt >= 0) {
          var prefix = line.text.substring(0, targetAt);
          var targetX = line.x;
          if (prefix) targetX = measureTextRight(doc, bodyStyleSource, prefix, line.x, line.y);
          duplicateTextLayer(doc, phoneticStyleSource, "@RUN_READING_PHONETIC_" + blockIndex + "_" + s, segment.text, targetX, line.y - lineGap);
          placed++;
          placedSegment = true;
          break;
        }
      }
      if (!placedSegment) {
        duplicateTextLayer(doc, phoneticStyleSource, "@RUN_READING_PHONETIC_" + blockIndex + "_" + s, segment.text, firstLineX, phoneticTop);
        TRACE.push("READING_PHONETIC_TARGET_MISSING block=" + blockIndex + " text=" + segment.text);
        placed++;
      }
    }
    if (!placed && block.phonetic) {
      duplicateTextLayer(doc, phoneticStyleSource, "@RUN_READING_PHONETIC_" + blockIndex, block.phonetic, firstLineX, phoneticTop);
    }
  }

  var placedBodyLines = 0;
  for (var i = 0; i < DATA.readingBlocks.length; i++) {
    var block = DATA.readingBlocks[i];
    var bodyTop = y + lineGap;
    var bodyLines = splitReadingBody(block.text || "", bodyTop);
    placeReadingPhoneticSegments(block, bodyLines, y, i);
    for (var w = 0; w < bodyLines.length; w++) {
      duplicateTextLayer(doc, bodyStyleSource, "@RUN_READING_BODY_" + i + "_" + w, bodyLines[w].text, bodyLines[w].x, bodyLines[w].y);
      placedBodyLines++;
    }
    y = bodyTop + lineGap * Math.max(bodyLines.length, 1);
    y += lineGap * Math.max(blockLineCount - 2, 0);
  }
  TRACE.push("READING_PLACED_BODY_LINES=" + placedBodyLines + " bottom=" + y + " firstLineX=" + firstLineX + " continuationX=" + continuationX);
}

function layoutDialogueLines(doc) {
  var metrics = DATA.dialogueMetrics;
  var roleX = metrics.roleX;
  var y = metrics.lineTop;
  var phoneticOffset = metrics.phoneticOffset;
  var dialogueGap = metrics.lineGap;
  var roleSpaceWidth = metrics.roleSpaceWidth;
  var maxRight = metrics.textMaxRight;
  var continuationX = metrics.continuationIndentX;
  var phoneticStyleSource = "@PART1_READING_LEFT_TEXT_STYLE_SOURCE";
  var roleStyleSource = "@PART1_DIALOGUE_SAMPLE_LINE_TEXT";
  var bodyStyleSource = "@PART1_DIALOGUE_INTRO_TEXT";
  requireStyleSource(doc, phoneticStyleSource);
  requireStyleSource(doc, roleStyleSource);
  requireStyleSource(doc, bodyStyleSource);
  var pendingPhonetic = "";
  var placedLines = 0;
  for (var i = 0; i < DATA.dialogueLines.length; i++) {
    var line = DATA.dialogueLines[i];
    if (line.kind === "phonetic") {
      pendingPhonetic = line.text;
      continue;
    }
    if (pendingPhonetic) {
      duplicateTextLayer(doc, phoneticStyleSource, "@RUN_DIALOGUE_PHONETIC_" + i, pendingPhonetic, roleX, y - phoneticOffset);
      pendingPhonetic = "";
    }
    var role = line.speaker ? line.speaker + ":" : "";
    var body = line.text || "";
    if (role && body.indexOf(role) === 0) body = body.substring(role.length).replace(/^\s+/, "");
    var roleWidth = metrics.roleWidths[role] || metrics.roleWidths["M:"];
    var bodyX = roleX + roleWidth + roleSpaceWidth;
    var firstLines = splitTextByMeasuredRight(doc, bodyStyleSource, body, bodyX, y, maxRight);
    var firstText = firstLines.length ? firstLines[0] : "";
    duplicateTextLayer(doc, roleStyleSource, "@RUN_DIALOGUE_ROLE_" + i, role, roleX, y);
    duplicateTextLayer(doc, bodyStyleSource, "@RUN_DIALOGUE_BODY_" + i + "_0", firstText, bodyX, y);
    placedLines++;
    var remaining = "";
    if (firstText && body.length > firstText.length) {
      remaining = body.substring(firstText.length).replace(/^\s+/, "");
    }
    var continuationLines = remaining ? splitTextByMeasuredRight(doc, bodyStyleSource, remaining, continuationX, y + dialogueGap, maxRight) : [];
    for (var c = 0; c < continuationLines.length; c++) {
      y += dialogueGap;
      duplicateTextLayer(doc, bodyStyleSource, "@RUN_DIALOGUE_BODY_" + i + "_" + (c + 1), continuationLines[c], continuationX, y);
      placedLines++;
    }
    y += dialogueGap;
  }
  TRACE.push("DIALOGUE_PLACED_LINES=" + placedLines + " bottom=" + y + " maxRight=" + maxRight + " continuationX=" + continuationX);
}

function savePsd(doc, path) {
  var opts = new PhotoshopSaveOptions();
  opts.layers = true;
  doc.saveAs(new File(path), opts, true, Extension.LOWERCASE);
}

function exportJpg(doc, path) {
  var opts = new ExportOptionsSaveForWeb();
  opts.format = SaveDocumentType.JPEG;
  opts.quality = 80;
  doc.exportDocument(new File(path), ExportType.SAVEFORWEB, opts);
}

function pageSpec(pageNo) {
  for (var i = 0; i < PLAN.pages.length; i++) {
    if (PLAN.pages[i].pageIndex === pageNo) return PLAN.pages[i];
  }
  throw new Error("Missing page spec " + pageNo);
}

function renderPage(pageNo, fillFn) {
  if (pageNo > MAX_PAGES_PER_LESSON) throw new Error("MAX_PAGES_PER_LESSON exceeded: " + pageNo);
  var spec = pageSpec(pageNo);
  log("OPEN_PAGE page=" + pageNo + " template=" + spec.template);
  var doc = app.open(new File(ROOT + "/" + spec.template));
  buildLayerMap(doc);
  unlockAll(doc);
  applyHiddenLayers(doc, spec);
  applyPart3SubtitlePolicy(doc, spec);
  setHeader(doc);
  setPageNo(doc, spec.pageNumbers[0], spec.pageNumbers[1]);
  fillFn(doc);
  var base = OUT + "/lesson_1_2_page_" + (pageNo < 10 ? "0" + pageNo : pageNo);
  log("SAVE_PAGE page=" + pageNo + " psd=" + base + ".psd");
  savePsd(doc, base + ".psd");
  log("EXPORT_JPG page=" + pageNo + " jpg=" + base + ".jpg");
  exportJpg(doc, base + ".jpg");
  doc.close(SaveOptions.DONOTSAVECHANGES);
  log("CLOSE_PAGE page=" + pageNo);
}

ensureFolder(ROOT + "/output");
ensureFolder(OUT);
if (PLAN.pages.length > MAX_PAGES_PER_LESSON) throw new Error("Plan pages exceed MAX_PAGES_PER_LESSON: " + PLAN.pages.length);
openLog();

renderPage(1, function(doc) {
  var spec = pageSpec(1);
  applyPart1Module(doc, spec);
  applyVocabModule(doc, spec, "part2_rows_01_08");
});

if (!RENDER_FIRST_PAGE_ONLY) {

renderPage(2, function(doc) {
  var spec = pageSpec(2);
  applyVocabModule(doc, spec, "part2_rows_09_21");
  setText(doc, "@PART3_LEAD_ORANGE_ITALIC_TEXT", DATA.grammarLead);
  setText(doc, "@PART3_BODY_TEXT_BLOCK_02", DATA.grammarP2A);
  setText(doc, "@PART3_BODY_TEXT_BLOCK_03", DATA.grammarP2B);
});

renderPage(3, function(doc) {
  setText(doc, "@PART3_CONT_TEXT_BLOCK_LEFT_01", DATA.grammarP3A);
  setText(doc, "@PART3_CONT_TEXT_BLOCK_LEFT_02", DATA.grammarP3B);
  setText(doc, "@PART3_CONT_TEXT_BLOCK_LEFT_03", DATA.grammarP3C);
  setText(doc, "@PART3_CONT_TEXT_BLOCK_RIGHT_01", DATA.grammarP3D);
  setText(doc, "@PART3_CONT_TEXT_BLOCK_RIGHT_02", "");
});

renderPage(4, function(doc) {
  setText(doc, "@PART3_CONT_TEXT_BLOCK_LEFT", DATA.grammarP4A);
  setText(doc, "@PART3_CONT_TEXT_BLOCK_RIGHT_TOP", DATA.grammarP4B);
  if (DATA.grammarOverflow && DATA.grammarOverflow.length) TRACE.push("REVIEW_GRAMMAR_OVERFLOW paragraphs=" + DATA.grammarOverflow.length);
  setText(doc, "@PART4_EXERCISE_Q1_NO_TEXT", DATA.exerciseSection1No);
  setText(doc, "@PART4_EXERCISE_Q1_BODY_TEXT", DATA.exerciseP4A);
  setText(doc, "@PART4_EXERCISE_Q2_NO_TEXT", DATA.exerciseSection2No);
  setText(doc, "@PART4_EXERCISE_Q2_BODY_TEXT", "");
});

renderPage(5, function(doc) {
  setText(doc, "@PART4_EXERCISE_CONT_BODY_TEXT", DATA.exerciseP4B);
});

}

var traceFile = new File(OUT + "/render_trace.txt");
traceFile.encoding = "UTF-8";
traceFile.open("w");
traceFile.write(TRACE.join("\n"));
traceFile.close();
closeLog();
