'use client'
import { useState, useCallback } from 'react'

// 蛻・ｊ霑斐＠繝・・繧ｿ
const OBJECTION_TREE: Record<string, { label: string; response: string }> = {
  // 笏笏 繧ｫ繝・ざ繝ｪ 笏笏
  'cat_busy':        { label: '竢ｰ 莉翫・蠢吶＠縺・, response: '' },
  'cat_nointerest':  { label: '・ 闊亥袖縺後↑縺・, response: '' },
  'cat_other':       { label: '召 莉也､ｾ繧剃ｽｿ縺｣縺ｦ縺・ｋ', response: '' },
  'cat_price':       { label: '超 鬮倥◎縺・・縺企≡縺後°縺九ｋ', response: '' },
  'cat_key':         { label: '泊 繧ｫ繝ｼ繝峨く繝ｼ縺ｧ縺ｪ縺・→繝繝｡', response: '' },
  'cat_custom':      { label: '妾 縺・■縺ｮ讌ｭ諷九↓蜷医ｏ縺ｪ縺・, response: '' },
  'cat_pms':         { label: '捗 PMS縺ｨ騾｣謳ｺ縺ｧ縺阪ｋ・・, response: '' },
  'cat_unmanned':    { label: '圻 辟｡莠ｺ縺ｫ縺ｯ縺ｧ縺阪↑縺・, response: '' },
  'cat_person':      { label: '瞳 諡・ｽ楢・ｸ榊惠', response: '' },
  'cat_email':       { label: '透 繝｡繝ｼ繝ｫ縺悟ｱ翫°縺ｪ縺・, response: '' },
  'cat_seminar':     { label: '套 繧ｻ繝溘リ繝ｼ縺ｮ譯亥・', response: '' },
  'cat_inbound':     { label: '件 繧､繝ｳ繝舌え繝ｳ繝牙ｯｾ蠢懊・・・, response: '' },
  'cat_size':        { label: '升 蟆剰ｦ乗ｨ｡縺縺九ｉ荳崎ｦ√〒縺ｯ・・, response: '' },
  'cat_timing':      { label: '宕 莉翫・讀懆ｨ取凾譛溘〒縺ｯ縺ｪ縺・, response: '' },
  'cat_claim':       { label: '丕 縺九￠縺ｦ縺上ｋ縺ｪ・医け繝ｬ繝ｼ繝・・, response: '' },

  // 笏笏 莉翫・蠢吶＠縺・笏笏
  'busy_later':        { label: '縺・▽鬆・↑繧牙､ｧ荳亥､ｫ縺狗｢ｺ隱阪☆繧・, response: '縲梧価遏･縺・◆縺励∪縺励◆縲ゅ〒縺ｯ縲√∪縺溘♀譎る俣縺ｮ繧医＞縺ｨ縺阪↓縺秘｣邨｡縺輔○縺ｦ縺・◆縺縺・※繧ゅｈ繧阪＠縺・〒縺励ｇ縺・°・溘＞縺､鬆・〒縺励◆繧峨ｈ繧阪＠縺・〒縺励ｇ縺・°・溘・ },
  'busy_short':        { label: '30遘偵□縺代♀鬘倥＞縺吶ｋ', response: '縲後♀蠢吶＠縺・→縺薙ｍ螟ｧ螟画＄繧悟・繧翫∪縺吶・0遘偵□縺代♀譎る俣縺・◆縺縺代∪縺吶〒縺励ｇ縺・°縲りｳ・侭繧偵Γ繝ｼ繝ｫ縺ｧ縺企√ｊ縺吶ｋ縺縺代〒繧ゅ√＆縺帙※縺・◆縺縺代ｌ縺ｰ縺ｨ諤昴▲縺ｦ縺翫ｊ縺ｾ縺吶ゅ・ },
  'busy_task':         { label: '繧ｿ繧ｹ繧ｯ縺ｫ謗ｧ縺医※蠕梧律縺九￠繧・, response: '縲後°縺励％縺ｾ繧翫∪縺励◆縲ゅ〒縺ｯ縲∝ｾ梧律縺ゅｉ縺溘ａ縺ｦ縺秘｣邨｡縺輔○縺ｦ縺・◆縺縺阪∪縺吶ゅ・・ｧ倥・縺雁錐蜑阪→縺秘｣邨｡蜈医∫｢ｺ隱阪＆縺帙※縺・◆縺縺・※繧医ｍ縺励＞縺ｧ縺励ｇ縺・°・溘・ },
  'busy_mail':         { label: '莉翫・雉・侭縺縺代Γ繝ｼ繝ｫ縺ｧ騾√ｋ', response: '縲後♀蠢吶＠縺・→縺薙ｍ螟ｱ遉ｼ縺・◆縺励∪縺励◆縲ゅ〒縺ｯ雉・侭縺縺代〒繧ゅΓ繝ｼ繝ｫ縺ｧ縺企√ｊ縺輔○縺ｦ縺・◆縺縺・※繧ゅｈ繧阪＠縺・〒縺励ｇ縺・°・溘Γ繝ｼ繝ｫ繧｢繝峨Ξ繧ｹ繧偵＞縺溘□縺代ｋ縺縺代〒螟ｧ荳亥､ｫ縺ｧ縺吶ゅ・ },
  'busy_time_ask':     { label: '莉頑律縺ｮ蠕悟濠縺ｫ蜀肴楔髮ｻ繧呈署譯・, response: '縲梧価遏･縺励∪縺励◆縲ゅ〒縺ｯ譛ｬ譌･縺ｮ蜊亥ｾ後・凾鬆・↓縺ゅｉ縺溘ａ縺ｦ縺企崕隧ｱ縺励※繧ゅｈ繧阪＠縺・〒縺励ｇ縺・°・・縲・蛻・□縺代＞縺溘□縺代ｌ縺ｰ蜊∝・縺ｧ縺吶ゅ・ },
  'busy_empathy':      { label: '郢∝ｿ呎悄縺ｧ縺ゅｋ縺薙→縺ｫ蜈ｱ諢溘＠縺ｦ谺｡縺ｫ縺､縺ｪ縺・, response: '縲檎ｹ∝ｿ呎悄縺ｧ縺雁ｿ吶＠縺・凾譛溘↓縺企崕隧ｱ縺励※縺励∪縺・筏縺苓ｨｳ縺ゅｊ縺ｾ縺帙ｓ縲ょｮ溘・郢∝ｿ呎悄縺薙◎蠑顔､ｾ陬ｽ蜩√′蜉帙ｒ逋ｺ謠ｮ縺吶ｋ縺ｮ縺ｧ縺吶′縲∬誠縺｡逹縺・◆繧ｿ繧､繝溘Φ繧ｰ縺ｧ荳蠎ｦ縺願ｩｱ縺励＆縺帙※縺・◆縺縺代∪縺吶〒縺励ｇ縺・°・溘・ },

  // 笏笏 闊亥袖縺後↑縺・笏笏
  'nointerest_reason':   { label: '蜈ｷ菴鍋噪縺ｪ逅・罰繧定◇縺・, response: '縲後◎縺・〒縺斐＊縺・∪縺吶°縲ょｷｮ縺玲髪縺医↑縺代ｌ縺ｰ縲√←縺ｮ繧医≧縺ｪ轤ｹ縺ｧ縺碑・蜻ｳ繧偵♀謖√■縺ｫ縺ｪ繧後↑縺・°縲∵蕗縺医※縺・◆縺縺代∪縺吶〒縺励ｇ縺・°・溘ｂ縺励さ繧ｹ繝磯擇繧・･ｭ諷九・蝠城｡後〒縺励◆繧峨∬ｧ｣豎ｺ縺ｧ縺阪◆莠倶ｾ九ｂ縺皮畑諢上＠縺ｦ縺翫ｊ縺ｾ縺吶ゅ・ },
  'nointerest_future':   { label: '蟆・擂逧・↑蜿ｯ閭ｽ諤ｧ繧堤｢ｺ隱・, response: '縲悟ｰ・擂逧・↓繧ゅ√＃闊亥袖縺ｯ縺ｪ縺・〒縺励ｇ縺・°・溯ｿ大ｹｴ縲∝・蝗ｽ縺九ｉ縺ｮ縺雁撫縺・粋繧上○縺悟悉蟷ｴ繧医ｊ縺九↑繧雁､壹￥縺ｪ縺｣縺ｦ縺阪※縺翫ｊ縺ｾ縺励※縲∵･ｭ逡悟・菴薙〒縺ｮ繧ｹ繧ｿ繝ｳ繝繝ｼ繝峨↓縺ｪ繧翫▽縺､縺ゅｊ縺ｾ縺吶ょ盾閠・ュ蝣ｱ縺縺代〒繧ゅ♀騾√ｊ縺輔○縺ｦ縺・◆縺縺代ｌ縺ｰ縺ｨ諤昴＞縺ｾ縺吶ゅ・ },
  'nointerest_seminar':  { label: '繧ｻ繝溘リ繝ｼ縺ｫ隱倥≧', response: '縲悟ｼ顔､ｾ縺ｯ騾ｱ2蝗槭√が繝ｳ繝ｩ繧､繝ｳ縺ｮ隱ｬ譏惹ｼ壹ｒ髢句ぎ縺励※縺翫ｊ縺ｾ縺呻ｼ域ｰｴ譖・1譎ゅ・驥第屆13譎ゑｼ峨・譎る俣遞句ｺｦ縺ｧ雋ｻ逕ｨ繝ｻ蟆主・莠倶ｾ九↑縺ｩ繧りｩｳ縺励￥縺碑ｪｬ譏弱〒縺阪∪縺吶ゅ＃蜿ょ刈縺ｯ辟｡譁吶〒縺吶・縺ｧ縲∽ｸ蠎ｦ縺・°縺後〒縺励ｇ縺・°・溘・ },
  'nointerest_flow':     { label: '豬∬｡後・豕｢繧剃ｼ昴∴繧・, response: '縲梧怙霑代ｈ縺上♀閠ｳ縺ｫ縺吶ｋ縺九→縺ｯ諤昴＞縺ｾ縺吶′縲∬・蜍輔メ繧ｧ繝・け繧､繝ｳ讖溘・莉ｶ縺ｫ縺ｪ繧翫∪縺吶ょ・蝗ｽ蜷・慍縺ｮ繝帙ユ繝ｫ讒倥〒諤･騾溘↓蟆主・縺碁ｲ繧薙〒縺翫ｊ縺ｾ縺励※縲∵･ｭ逡後・繧ｹ繧ｿ繝ｳ繝繝ｼ繝峨↓縺ｪ繧翫▽縺､縺ゅｋ迥ｶ豕√〒縺斐＊縺・∪縺吶ゆｻ也､ｾ讒倥↓驕・ｌ繧偵→繧峨↑縺・◆繧√↓繧ゅ∽ｸ蠎ｦ縺疲､懆ｨ弱＞縺溘□縺代∪縺帙ｓ縺具ｼ溘・ },
  'nointerest_info':     { label: '諠・ｱ縺縺代〒繧る√ｋ謠先｡・, response: '縲後＃闊亥袖縺後↑縺・・縺ｯ謇ｿ遏･縺・◆縺励∪縺励◆縲ゅ◆縺縲∬ｳ・侭縺縺代〒繧ゅ＃隕ｧ縺・◆縺縺代∪縺吶→縲∝・菴鍋噪縺ｪ繧ｳ繧ｹ繝医ｄ莉慕ｵ・∩縺後ｈ縺上ｏ縺九ｊ縺ｾ縺吶ゅΓ繝ｼ繝ｫ繧｢繝峨Ξ繧ｹ繧偵♀謨吶∴縺・◆縺縺代ｌ縺ｰ莉頑律荳ｭ縺ｫ縺企√ｊ縺・◆縺励∪縺吶ゅ・ },
  'nointerest_subsidy':  { label: 'IT陬懷勧驥代・隧ｱ縺ｫ蛻・ｊ譖ｿ縺医ｋ', response: '縲瑚｣ｽ蜩√・縺碑・蜻ｳ繧医ｊ蜈医↓縲∽ｻ雁ｹｴ縺ｮIT陬懷勧驥代・邱繧∝・繧翫′霑代▼縺・※縺・ｋ縺ｮ縺ｧ縺疲｡亥・縺励※縺・ｋ縺ｨ縺・≧蛛ｴ髱｢繧ゅ＃縺悶＞縺ｾ縺吶り｣懷勧驥醍筏隲九□縺代〒繧ょｼ顔､ｾ縺御ｻ｣陦後〒縺阪∪縺吶・縺ｧ縲∵ュ蝣ｱ縺縺代〒繧ょ女縺大叙縺｣縺ｦ縺・◆縺縺代∪縺吶〒縺励ｇ縺・°・溘・ },
  'nointerest_competitor': { label: '遶ｶ蜷医↓蟾ｮ繧偵▽縺代ｉ繧後ｋ蜑阪↓縲√→險ｴ豎・, response: '縲悟酔縺伜慍蝓溘・遶ｶ蜷医・繝・Ν讒倥′縺吶〒縺ｫ蟆主・縺輔ｌ縺ｦ縺・ｋ莠倶ｾ九ｂ縺斐＊縺・∪縺吶ゅメ繧ｧ繝・け繧､繝ｳ縺ｮ繧ｹ繝繝ｼ繧ｺ縺輔・蜿｣繧ｳ繝溘↓繧ょｽｱ髻ｿ縺励∪縺吶・縺ｧ縲∵ュ蝣ｱ縺縺代〒繧よ戟縺｣縺ｦ縺翫＞縺ｦ縺・◆縺縺代ｋ縺ｨ蟷ｸ縺・〒縺吶ゅ・ },

  // 笏笏 莉也､ｾ菴ｿ逕ｨ荳ｭ 笏笏
  'other_maker':       { label: '縺ｩ縺ｮ繝｡繝ｼ繧ｫ繝ｼ縺玖◇縺・, response: '縲後≠縲√◎縺・〒縺斐＊縺・∪縺励◆縺九ょｷｮ縺玲髪縺医↑縺代ｌ縺ｰ縲√←縺｡繧峨・繝｡繝ｼ繧ｫ繝ｼ讒倥ｒ縺泌茜逕ｨ縺輔ｌ縺ｦ縺・ｋ縺九∝盾閠・∪縺ｧ縺ｫ謨吶∴縺ｦ鬆ゅ￠縺ｾ縺吶〒縺励ｇ縺・°・溘・ },
  'other_compare':     { label: '豈碑ｼ・署譯医↓謖√■霎ｼ繧', response: '縲後☆縺ｧ縺ｫ蟆主・縺輔ｌ縺ｦ縺・ｉ縺｣縺励ｃ繧九・縺ｧ縺吶・縲ょｼ顔､ｾ縺ｯ閾ｪ遉ｾ髢狗匱縺ｮ縺溘ａ縲∽ｻ也､ｾ讒倥↓縺ｯ縺ｪ縺・ｩ溯・・医す繝ｪ繝ｳ繝繝ｼ骭蟇ｾ蠢懊・螳悟・繧ｪ繝ｼ繝繝ｼ繝｡繧､繝峨き繧ｹ繧ｿ繝槭う繧ｺ遲会ｼ峨′縺斐＊縺・∪縺吶ら樟迥ｶ縺ｮ隱ｲ鬘後′縺ゅｌ縺ｰ縲∵ｯ碑ｼ・ｳ・侭縺ｨ縺励※縺碑ｦｧ縺・◆縺縺代∪縺吶〒縺励ｇ縺・°・溘・ },
  'other_renewal':     { label: '譖ｴ譁ｰ繝ｻ繝ｪ繝励Ξ繧､繧ｹ謠先｡・, response: '縲檎樟蝨ｨ縺泌茜逕ｨ縺ｮ繧ｷ繧ｹ繝・Β縺ｮ螂醍ｴ・峩譁ｰ譎よ悄縺ｯ縺・▽鬆・〒縺励ｇ縺・°・溷ｼ顔､ｾ縺ｯ萓｡譬ｼ髱｢縺ｧ繧ゅ＃螂ｽ隧輔ｒ縺・◆縺縺・※縺翫ｊ縲∽ｹ励ｊ謠帙∴繧呈､懆ｨ弱＆繧後※縺・ｋ譁ｽ險ｭ讒倥ｂ蠅励∴縺ｦ縺翫ｊ縺ｾ縺吶ゅ■繧・≧縺ｩ縺昴・繧ｿ繧､繝溘Φ繧ｰ縺ｧ豈碑ｼ・､懆ｨ弱＞縺溘□縺代ｋ縺ｨ蟷ｸ縺・〒縺吶ゅ・ },
  'other_weakness':    { label: '迴ｾ蝨ｨ縺ｮ隱ｲ鬘後・荳肴ｺ繧定◇縺・, response: '縲檎樟蝨ｨ縺贋ｽｿ縺・・繧ｷ繧ｹ繝・Β縺ｧ縲∽ｽ輔°荳肴ｺ縺ｪ轤ｹ繧・後％縺薙′繧ゅ≧蟆代＠窶ｦ縲阪→縺・≧驛ｨ蛻・・縺斐＊縺・∪縺吶〒縺励ｇ縺・°・溷ｼ顔､ｾ縺ｯ繧ｫ繧ｹ繧ｿ繝槭う繧ｺ諤ｧ縺ｨ萓｡譬ｼ髱｢縺ｧ驕ｸ縺ｰ繧後ｋ縺薙→縺悟､壹￥縲∵隼蝟・〒縺阪ｋ蜿ｯ閭ｽ諤ｧ縺後≠繧九°繧ゅ＠繧後∪縺帙ｓ縲ゅ・ },
  'other_coexist':     { label: '菴ｵ逕ｨ繝ｻ陬懷ｮ梧署譯医ｒ縺吶ｋ', response: '縲後メ繧ｧ繝・け繧､繝ｳ讖溘・譌｢蟄倥・PMS繧・ｮ｡逅・す繧ｹ繝・Β縺ｨ縺ｮ騾｣謳ｺ繧ょ庄閭ｽ縺ｧ縺吶ゆｻ翫♀菴ｿ縺・・繧ｷ繧ｹ繝・Β縺ｯ縺昴・縺ｾ縺ｾ縺ｧ縲√メ繧ｧ繝・け繧､繝ｳ繝ｻ貂・ｮ励□縺大ｼ顔､ｾ陬ｽ蜩√ｒ菴ｿ縺｣縺ｦ縺・◆縺縺丞ｽ｢繧る∈謚櫁い縺ｨ縺励※縺斐＊縺・∪縺吶ゅ・ },

  // 笏笏 萓｡譬ｼ 笏笏
  'price_subsidy':     { label: 'IT陬懷勧驥代ｒ譯亥・縺吶ｋ', response: '縲悟ｼ顔､ｾ縺瑚｣懷勧驥醍筏隲九ｒ莉｣陦後〒縺阪∪縺吶・T陬懷勧驥第ｴｻ逕ｨ縺ｧKIOSK遲蝉ｽ薙′譛螳・8荳・・縲懊√ち繝悶Ξ繝・ヨ蝙九・13荳・・縲懊〒縺泌ｰ主・蜿ｯ閭ｽ縺ｧ縺吶り｣懷勧驥代′縺ゅｌ縺ｰ螳溯ｳｪ雋ｻ逕ｨ縺後°縺ｪ繧頑椛縺医ｉ繧後∪縺吶りｩｳ縺励＞雉・侭繧偵♀騾√ｊ縺励※繧ゅｈ繧阪＠縺・〒縺励ｇ縺・°・溘・ },
  'price_running':     { label: '譛磯｡崎ｲｻ逕ｨ繝ｻ繧ｳ繧ｹ繝亥炎貂帛柑譫懊ｒ隱ｬ譏・, response: '縲梧怦鬘崎ｲｻ逕ｨ縺ｯKIOSK蝙九〒19,600蜀・ｼ矩Κ螻区焚ﾃ・00蜀・√ち繝悶Ξ繝・ヨ蝙九・1螳､500蜀・〒縺吶らｹ∝ｿ呎悄縺ｮ縺ｿ菴ｿ逕ｨ縺ｧ菴ｿ繧上↑縺・怦縺ｯ0蜀・∵律蜑ｲ繧願ｨ育ｮ励ｂ蜿ｯ閭ｽ縺ｧ縺吶ゆｸ譁ｹ縺ｧ縲√ヵ繝ｭ繝ｳ繝医せ繧ｿ繝・ヵ縺ｮ莠ｺ莉ｶ雋ｻ蜑頑ｸ帛柑譫懊→豈斐∋繧九→縲∝､壹￥縺ｮ譁ｽ險ｭ讒倥〒蜊雁ｹｴ縲・蟷ｴ莉･蜀・↓蝗槫庶縺輔ｌ縺ｦ縺・∪縺吶ゅ・ },
  'price_season':      { label: '蟄｣遽髯仙ｮ壹・繝ｩ繝ｳ繧呈｡亥・', response: '縲後＃菴ｿ逕ｨ縺ｫ縺ｪ繧峨↑縺・怦縺ｯ譛磯｡・蜀・↓縺ｪ繧翫∪縺吶らｹ∝ｿ呎悄縺ｮ縺ｿ縺ｮ縺泌茜逕ｨ繧・∝悄譌･逾昴・縺ｿ縺比ｽｿ逕ｨ縺ｮ譌･蜑ｲ繧願ｨ育ｮ励・繝ｩ繝ｳ繧ゅ＃縺悶＞縺ｾ縺吶ょｮ滄圀縺ｮ雋ｻ逕ｨ諢溘ｒ繝｡繝ｼ繝ｫ縺ｧ縺疲｡亥・縺励※繧ゅｈ繧阪＠縺・〒縺励ｇ縺・°・溘・ },
  'price_small':       { label: '蟆剰ｦ乗ｨ｡蜷代￠菴弱さ繧ｹ繝医・繝ｩ繝ｳ繧呈署遉ｺ', response: '縲悟ｰ剰ｦ乗ｨ｡譁ｽ險ｭ讒伜髄縺代↓縺ｯ縲√ち繝悶Ξ繝・ヨ蝙九〒縺泌ｰ主・縺・◆縺縺代∪縺吶ょ・譛溯ｲｻ逕ｨ縺ｯIT陬懷勧驥第ｴｻ逕ｨ縺ｧ13荳・・縲懊∵怦鬘阪・1螳､500蜀・〒縺吶ゆｸ霆貞ｮｶ繧・ｰ剰ｦ乗ｨ｡譌・､ｨ讒倥↓繧ょｰ主・螳溽ｸｾ縺後＃縺悶＞縺ｾ縺吶ゅ・ },
  'price_roi':         { label: '莠ｺ莉ｶ雋ｻ蜑頑ｸ娚OI繧定ｪｬ譏弱☆繧・, response: '縲御ｻｮ縺ｫ繝輔Ο繝ｳ繝医せ繧ｿ繝・ヵ1蜷阪・螟憺俣蟇ｾ蠢懊ｒ蜑頑ｸ帙〒縺阪◆縺ｨ縺吶ｋ縺ｨ縲∵怦20縲・0荳・・縺ｮ莠ｺ莉ｶ雋ｻ蜑頑ｸ帙↓縺ｪ繧翫∪縺吶よ怦鬘崎ｲｻ逕ｨ縺ｨ豈碑ｼ・☆繧九→縲∝､壹￥縺ｮ譁ｽ險ｭ讒倥〒3縲・繝ｶ譛医〒蝗槫庶縺ｧ縺阪※縺・∪縺吶ゅ・ },
  'price_subsidy_detail': { label: 'IT陬懷勧驥代・隧ｳ邏ｰ繧定ｪｬ譏弱☆繧・, response: '縲栗T蟆主・陬懷勧驥代・荳ｭ蟆丈ｼ∵･ｭ縺栗T繧ｷ繧ｹ繝・Β繧貞ｰ主・縺吶ｋ髫帙↓蝗ｽ縺梧怙螟ｧ2/3繧定｣懷勧縺吶ｋ蛻ｶ蠎ｦ縺ｧ縺吶ょｼ顔､ｾ縺ｯ陬懷勧驥醍筏隲九・莉｣陦後°繧画嶌鬘樔ｽ懈・縺ｾ縺ｧ蜈ｨ縺ｦ蟇ｾ蠢懊＠縺ｦ縺翫ｊ縲∝ｾ｡遉ｾ縺ｫ縺碑ｲ諡・＞縺溘□縺上・縺ｯ蠢・ｦ∵嶌鬘槭・縺疲署蜃ｺ縺ｮ縺ｿ縺ｧ縺吶ゅ・ },

  // 笏笏 繧ｫ繝ｼ繝峨く繝ｼ繝ｻ骰ｵ 笏笏
  'key_cylinder':      { label: '繧ｷ繝ｪ繝ｳ繝繝ｼ骭蟇ｾ蠢懊ｒPR', response: '縲悟ｼ顔､ｾ縺ｮ蠑ｷ縺ｿ縺ｯ縲√す繝ｪ繝ｳ繝繝ｼ骭・育黄逅・く繝ｼ・峨↓繧ょｯｾ蠢懷庄閭ｽ縺ｪ縺薙→縺ｧ縺呻ｼ∝挨螢ｲ繧翫・繧ｭ繝ｼ繝懊ャ繧ｯ繧ｹ繧剃ｽｿ縺・％縺ｨ縺ｧ縲∵ｸ・ｮ励′螳御ｺ・☆繧九→閾ｪ蜍輔〒繧ｭ繝ｼ繝懊ャ繧ｯ繧ｹ縺碁幕縺阪√♀螳｢讒倥′繧ｻ繝ｫ繝輔〒骰ｵ繧偵♀蜿励￠蜿悶ｊ縺・◆縺縺代∪縺吶ゅき繝ｼ繝峨く繝ｼ縺ｸ縺ｮ螟画峩縺ｯ荳蛻・ｸ崎ｦ√〒縺吶ゅ・ },
  'key_smartlock':     { label: '繧ｯ繝ｩ繧ｦ繝峨せ繝槭・繝医Ο繝・け繧呈署譯・, response: '縲後け繝ｩ繧ｦ繝峨せ繝槭・繝医Ο繝・け縺ｨ縺・≧驕ｸ謚櫁い繧ゅ＃縺悶＞縺ｾ縺吶よ囓險ｼ逡ｪ蜿ｷ縺ｧ髢矩権縺ｧ縺阪√メ繧ｧ繝・け繧､繝ｳ讖溘°繧画賜蜃ｺ縺輔ｌ繧九Ξ繧ｷ繝ｼ繝医↓證苓ｨｼ逡ｪ蜿ｷ縺瑚・蜍輔〒蜊ｰ蟄励＆繧後∪縺吶る嵯縺ｮ蜿励￠貂｡縺励′螳悟・縺ｫ繧ｻ繝ｫ繝輔↓縺ｪ繧翫∪縺吶ゅ・ },
  'key_receipt':       { label: '繝ｬ繧ｷ繝ｼ繝暗怜ｯｾ髱｢譁ｹ蠑上ｒ謠先｡・, response: '縲後ｂ縺玲磁螳｢繧呈ｮ九＠縺溘＞蝣ｴ蜷医・縲√メ繧ｧ繝・け繧､繝ｳ讖溘〒貂・ｮ励∪縺ｧ貂医∪縺帙※繝ｬ繧ｷ繝ｼ繝医ｒ逋ｺ陦後＠縲√◎縺ｮ繝ｬ繧ｷ繝ｼ繝医ｒ繝輔Ο繝ｳ繝医〒骰ｵ縺ｨ莠､謠帙☆繧九→縺・≧驕狗畑繧ょ庄閭ｽ縺ｧ縺吶ょｯｾ髱｢縺ｮ謗･螳｢隕∫ｴ繧呈ｮ九＠縺ｪ縺後ｉ縲∵焔邯壹″縺縺大柑邇・喧縺ｧ縺阪∪縺吶ゅ・ },
  'key_keybox':        { label: '繧ｭ繝ｼ繝懊ャ繧ｯ繧ｹ縺ｮ莉慕ｵ・∩繧定ｪｬ譏弱☆繧・, response: '縲後く繝ｼ繝懊ャ繧ｯ繧ｹ縺ｯ螢√↓險ｭ鄂ｮ縺吶ｋ骰ｵ縺ｮ蜿守ｴ阪・繝・け繧ｹ縺ｧ縲√メ繧ｧ繝・け繧､繝ｳ讖溘〒縺ｮ貂・ｮ怜ｮ御ｺ・→蜷梧凾縺ｫ閾ｪ蜍戊ｧ｣骭縺輔ｌ縺ｾ縺吶ら分蜿ｷ骭縺ｧ縺ｯ縺ｪ縺剰・蜍戊ｧ｣骭蝙九↑縺ｮ縺ｧ縲√♀螳｢讒倥′證苓ｨｼ逡ｪ蜿ｷ繧定ｦ壹∴繧句ｿ・ｦ√′縺ゅｊ縺ｾ縺帙ｓ縲ゅ・ },
  'key_cost':          { label: '繧ｫ繝ｼ繝峨く繝ｼ蛹悶・繧ｳ繧ｹ繝医ｒ豈碑ｼ・☆繧・, response: '縲後き繝ｼ繝峨く繝ｼ縺ｸ縺ｮ螟画峩縺ｯ險ｭ蛯呎兜雉・′蠢・ｦ√〒縺吶′縲∝ｼ顔､ｾ縺ｮ繧ｷ繝ｪ繝ｳ繝繝ｼ骭蟇ｾ蠢懊↑繧画里蟄倥・骰ｵ繧偵◎縺ｮ縺ｾ縺ｾ菴ｿ縺医∪縺吶ゆｽ呵ｨ医↑謾ｹ菫ｮ雋ｻ逕ｨ繧偵°縺代★縺ｫ繝√ぉ繝・け繧､繝ｳ讖溘ｒ蟆主・縺ｧ縺阪ｋ縺ｮ縺悟ｼ顔､ｾ縺ｮ蠑ｷ縺ｿ縺ｧ縺吶ゅ・ },

  // 笏笏 讌ｭ諷九・繧ｫ繧ｹ繧ｿ繝槭う繧ｺ 笏笏
  'custom_order':      { label: '繧ｪ繝ｼ繝繝ｼ繝｡繧､繝峨ｒPR', response: '縲梧勸谿ｵ繧ｹ繧ｿ繝・ヵ縺悟哨鬆ｭ縺ｧ縺碑ｪｬ譏弱＠縺ｦ縺・ｋ縺薙→繧偵√メ繧ｧ繝・け繧､繝ｳ讖溘↓繧ｫ繧ｹ繧ｿ繝槭う繧ｺ縺励※邨・∩霎ｼ繧縺薙→縺悟庄閭ｽ縺ｧ縺吶ょｼ顔､ｾ縺ｯ閾ｪ遉ｾ髢狗匱縺ｮ縺溘ａ縲∝ｾ｡遉ｾ蟆ら畑縺ｮ繧ｪ繝ｼ繝繝ｼ繝｡繧､繝峨ｒ縺疲署萓帙〒縺阪∪縺吶ゆｻ也､ｾ讒倥↓縺ｯ逵滉ｼｼ縺ｮ縺ｧ縺阪↑縺・ｼｷ縺ｿ縺ｧ縺吶ゅ・ },
  'custom_example':    { label: '蜷梧･ｭ諷九・蟆主・莠倶ｾ九ｒ謠千､ｺ', response: '縲悟ｼ顔､ｾ縺ｧ縺ｯ謗･螳｢縺ｮ雉ｪ繧定誠縺ｨ縺輔★縺ｫ謇狗ｶ壹″縺縺代ｒ繧ｹ繝槭・繝亥喧縺励※縲・｡ｧ螳｢貅雜ｳ蠎ｦ繧剃ｸ翫￡縺滉ｺ倶ｾ九′縺斐＊縺・∪縺吶ょ酔縺倥ｈ縺・↑讌ｭ諷九・譁ｽ險ｭ讒倥・蟆主・莠倶ｾ九ｒ雉・侭縺ｧ縺企√ｊ縺励※繧ゅｈ繧阪＠縺・〒縺励ｇ縺・°・溘・ },
  'custom_ryokan':     { label: '譌・､ｨ繝ｻ貂ｩ豕画命險ｭ縺ｸ縺ｮ蟇ｾ蠢・, response: '縲梧羅鬢ｨ讒倥〒繧ょ､壽焚縺泌ｰ主・縺・◆縺縺・※縺翫ｊ縺ｾ縺吶よ律蟶ｰ繧頑ｸｩ豕牙ｮ｢縺ｮ蜿嶺ｻ倥・貂・ｮ励∵悃鬟溷虻繝ｻ螟暮｣溷虻縺ｮ逋ｺ陦後↑縺ｩ縲∵羅鬢ｨ迚ｹ譛峨・驕狗畑縺ｫ繧ゅき繧ｹ繧ｿ繝槭う繧ｺ蟇ｾ蠢懊〒縺阪∪縺吶ゅ♀隧ｱ縺励□縺代〒繧ゅ＞縺九′縺ｧ縺励ｇ縺・°・溘・ },
  'custom_hospi':      { label: '繝帙せ繝斐ち繝ｪ繝・ぅ繧定誠縺ｨ縺輔↑縺・ｨｴ豎・, response: '縲後メ繧ｧ繝・け繧､繝ｳ讖溘ｒ蟆主・縺吶ｋ縺薙→縺ｧ縲√ヵ繝ｭ繝ｳ繝医せ繧ｿ繝・ヵ縺後メ繧ｧ繝・け繧､繝ｳ謇狗ｶ壹″縺九ｉ隗｣謾ｾ縺輔ｌ縲∬ｦｳ蜈画｡亥・繧・♀蜃ｺ霑弱∴縺ｪ縺ｩ縺ｮ譛ｬ譚･縺ｮ謗･螳｢縺ｫ髮・ｸｭ縺ｧ縺阪ｋ繧医≧縺ｫ縺ｪ繧翫∪縺吶らｵ先棡縺ｨ縺励※繝帙せ繝斐ち繝ｪ繝・ぅ縺悟髄荳翫＠縺滓命險ｭ讒倥ｂ螟壹￥縺・ｉ縺｣縺励ｃ縺・∪縺吶ゅ・ },
  'custom_demo':       { label: '繝・Δ讖溘・螳滓ｩ溽｢ｺ隱阪ｒ謠先｡・, response: '縲悟ｮ滄圀縺ｮ謫堺ｽ懈─縺梧ｰ励↓縺ｪ繧九ｈ縺・〒縺励◆繧峨√が繝ｳ繝ｩ繧､繝ｳ繝・Δ繧偵＃逕ｨ諢上☆繧九％縺ｨ繧ょ庄閭ｽ縺ｧ縺吶ょｮ滄圀縺ｮ逕ｻ髱｢繧偵＃隕ｧ縺・◆縺縺阪↑縺後ｉ縲∝ｾ｡遉ｾ縺ｮ讌ｭ諷九↓蜷医≧險ｭ螳壹ｒ縺疲署譯医〒縺阪∪縺吶・0蛻・ｨ句ｺｦ縺ｧ貂医∩縺ｾ縺吶′縲√＞縺九′縺ｧ縺励ｇ縺・°・溘・ },
  'custom_ui':         { label: 'UI繝ｻ逕ｻ髱｢縺ｮ繧ｫ繧ｹ繧ｿ繝槭う繧ｺ繧定ｪｬ譏・, response: '縲後メ繧ｧ繝・け繧､繝ｳ逕ｻ髱｢縺ｮUI縺ｯ蠕｡遉ｾ縺ｮ繝悶Λ繝ｳ繝峨↓蜷医ｏ縺帙※繧ｫ繧ｹ繧ｿ繝槭う繧ｺ縺ｧ縺阪∪縺吶ゅΟ繧ｴ繧・牡蜻ｳ縲∬｡ｨ遉ｺ縺吶ｋ雉ｪ蝠城・岼縲∝ｮｿ豕顔ｴ・ｬｾ縺ｮ蜀・ｮｹ縺ｪ縺ｩ繧ょ､画峩蜿ｯ閭ｽ縺ｧ縺吶ゅ後≧縺｡繧峨＠縺上↑縺・阪→縺ｯ縺ｪ繧翫∪縺帙ｓ縲ゅ・ },

  // 笏笏 PMS騾｣謳ｺ 笏笏
  'pms_list':          { label: 'PMS騾｣謳ｺ螳溽ｸｾ繧呈｡亥・', response: '縲悟ｼ顔､ｾ縺ｯPMS・医・繝・Ν繧ｷ繧ｹ繝・Β・峨→縺ｮ騾｣謳ｺ髢狗匱縺ｫ霑大ｹｴ蜉帙ｒ蜈･繧後※縺・∪縺吶る｣謳ｺ螳溽ｸｾ・壹せ繝・う繧ｷ繝ｼ繝ｻ繧ｹ繧､繝ｼ繝医ヶ繝・け繝ｻ繝吶ャ繝・4縲ら樟蝨ｨ繧り､・焚縺ｮPMS縺ｨ騾｣謳ｺ髢狗匱縺碁ｲ陦御ｸｭ縺ｧ縺吶ょｾ｡遉ｾ縺ｮPMS縺ｫ縺､縺・※繧ゅ√●縺ｲ荳蠎ｦ縺皮嶌隲・＞縺溘□縺代∪縺吶〒縺励ｇ縺・°・溘・ },
  'pms_develop':       { label: '騾｣謳ｺ髢狗匱縺ｮ諢乗ｬｲ繧剃ｼ昴∴繧・, response: '縲後♀螳｢讒倥・縺碑ｦ∵悍縺ｫ繧医ｊ縺九↑繧翫・鬆ｻ蠎ｦ縺ｧ騾｣謳ｺ髢狗匱縺碁ｲ繧薙〒縺・∪縺吶・縺ｧ縲∝ｾ｡遉ｾ縺ｮPMS繧ゆｻ雁ｾ碁｣謳ｺ髢狗匱繧帝ｲ繧√ｋ縺薙→縺悟庄閭ｽ縺ｧ縺吶ゅ∪縺壹・繧ｷ繧ｹ繝・Β蜷阪ｒ縺頑蕗縺医＞縺溘□縺代∪縺吶〒縺励ｇ縺・°・溘・ },
  'pms_standalone':    { label: 'PMS騾｣謳ｺ縺ｪ縺励〒繧ゆｽｿ縺医ｋ縺ｨ莨昴∴繧・, response: '縲訓MS縺ｨ縺ｮ騾｣謳ｺ縺後↑縺上※繧ゅ∝ｼ顔､ｾ陬ｽ蜩∝腰菴薙〒繝√ぉ繝・け繧､繝ｳ繝ｻ貂・ｮ励・邊ｾ邂玲嶌逋ｺ陦後∪縺ｧ螳檎ｵ舌〒縺阪∪縺吶る｣謳ｺ縺後↑縺・ｴ蜷医〒繧ゅ∽ｺ育ｴ・分蜿ｷ縺ｧ縺ｮ辣ｧ蜷医ｄ謇句虚蜈･蜉帙〒縺ｮ驕狗畑縺悟庄閭ｽ縺ｧ縺吶ゅ∪縺壼渕譛ｬ讖溯・繧定ｩｦ縺励※縺・◆縺縺・※縺九ｉ騾｣謳ｺ繧呈､懆ｨ弱☆繧区命險ｭ讒倥ｂ螟壹＞縺ｧ縺吶ゅ・ },
  'pms_api':           { label: 'API騾｣謳ｺ縺ｮ莉慕ｵ・∩繧定ｪｬ譏弱☆繧・, response: '縲窟PI縺悟・髢九＆繧後※縺・ｋPMS縺ｧ縺ゅｌ縺ｰ縲∝ｼ顔､ｾ縺ｨ縺ｮ騾｣謳ｺ髢狗匱縺後〒縺阪∪縺吶ょｾ｡遉ｾ縺ｮPMS縺ｮAPI莉墓ｧ俶嶌繧堤｢ｺ隱阪〒縺阪ｌ縺ｰ縲・｣謳ｺ蜿ｯ閭ｽ縺九←縺・°繧貞ｼ顔､ｾ繧ｨ繝ｳ繧ｸ繝九い縺檎｢ｺ隱阪＞縺溘＠縺ｾ縺吶１MS縺ｮ繧ｷ繧ｹ繝・Β蜷阪ｒ謨吶∴縺ｦ縺・◆縺縺代∪縺吶〒縺励ｇ縺・°・溘・ },

  // 笏笏 辟｡莠ｺ蛹・笏笏
  'unmanned_pr':       { label: '逵∽ｺｺ蛹悶・蜉ｹ邇・喧縺ｫ險縺・鋤縺医ｋ', response: '縲後檎┌莠ｺ蛹悶阪→縺・≧繧医ｊ縲√檎怐莠ｺ蛹悶阪・縲梧･ｭ蜍吝柑邇・喧縲阪・繝・・繝ｫ縺ｨ縺励※縺疲ｴｻ逕ｨ縺・◆縺縺・※縺翫ｊ縺ｾ縺吶ゅヵ繝ｭ繝ｳ繝医せ繧ｿ繝・ヵ縺後メ繧ｧ繝・け繧､繝ｳ謇狗ｶ壹″縺九ｉ隗｣謾ｾ縺輔ｌ繧九％縺ｨ縺ｧ縲√♀螳｢讒倥→縺ｮ莨夊ｩｱ繧・ｦｳ蜈画｡亥・縺ｪ縺ｩ縲∵悽譚･縺ｮ謗･螳｢繧ｵ繝ｼ繝薙せ縺ｫ繧医ｊ髮・ｸｭ縺ｧ縺阪ｋ繧医≧縺ｫ縺ｪ繧翫∪縺吶ゅ・ },
  'unmanned_night':    { label: '螟憺俣繝ｻ豺ｱ螟懷ｸｯ縺ｮ蟇ｾ蠢懊→縺励※險ｴ豎・, response: '縲檎音縺ｫ螟憺俣繧・ｷｱ螟懷ｸｯ縺ｮ繝√ぉ繝・け繧､繝ｳ縺ｧ蜉ｹ譫懊ｒ逋ｺ謠ｮ縺励∪縺吶ゅせ繧ｿ繝・ヵ縺御ｸ榊惠縺ｮ譎る俣縺ｧ繧ゅ√♀螳｢讒倥′閾ｪ蛻・〒繝√ぉ繝・け繧､繝ｳ縺ｧ縺阪ｋ縺溘ａ縲∵ｷｱ螟懊・繝輔Ο繝ｳ繝亥ｯｾ蠢懊ｒ螟ｧ蟷・↓蜑頑ｸ帙〒縺阪∪縺吶ゅ・ },
  'unmanned_inbound':  { label: '繧､繝ｳ繝舌え繝ｳ繝峨∈縺ｮ蟇ｾ蠢懷鴨', response: '縲悟､門嵜隱槫ｯｾ蠢懶ｼ・3縺句嵜隱橸ｼ峨→繝代せ繝昴・繝医せ繧ｭ繝｣繝ｳ讖溯・縺ｫ繧医ｊ縲√う繝ｳ繝舌え繝ｳ繝峨・縺雁ｮ｢讒倥ｂ繧ｹ繝繝ｼ繧ｺ縺ｫ繝√ぉ繝・け繧､繝ｳ縺ｧ縺阪∪縺吶りｨ隱槭・螢√′縺ｪ縺上↑繧九％縺ｨ縺ｧ縲√せ繧ｿ繝・ヵ縺ｮ蟇ｾ蠢懆ｲ諡・′螟ｧ蟷・↓貂帙ｊ縺ｾ縺吶ゅ・ },
  'unmanned_hybrid':   { label: '繝上う繝悶Μ繝・ラ驕狗畑繧呈署譯・, response: '縲悟ｮ悟・辟｡莠ｺ蛹悶〒縺ｯ縺ｪ縺上√ワ繧､繝悶Μ繝・ラ驕狗畑繧ょ庄閭ｽ縺ｧ縺吶ゆｾ九∴縺ｰ蟷ｳ譌･譏ｼ縺ｯ繝輔Ο繝ｳ繝亥ｯｾ蠢懊∵ｷｱ螟懊ｄ郢∝ｿ呎悄縺ｯ繝√ぉ繝・け繧､繝ｳ讖溘ｒ菴ｵ逕ｨ縲√→縺・≧蠖｢縺ｧ縺吶ら憾豕√↓蜷医ｏ縺帙※譟碑ｻ溘↓菴ｿ縺・・縺代ｉ繧後∪縺吶ゅ・ },
  'unmanned_elderly':  { label: '縺雁ｹｴ蟇・ｊ繧ｲ繧ｹ繝医∈縺ｮ蟇ｾ蠢懊ｒ隱ｬ譏・, response: '縲後＃蟷ｴ驟阪・縺雁ｮ｢讒倥↓縺ｯ繧ｹ繧ｿ繝・ヵ縺後し繝昴・繝医☆繧矩°逕ｨ縺ｫ縺励※縺・ｋ譁ｽ險ｭ讒倥ｂ螟壹＞縺ｧ縺吶よｩ滓｢ｰ縺瑚協謇九↑縺雁ｮ｢讒倥↓縺ｯ繝輔Ο繝ｳ繝医〒蟇ｾ蠢懊＠縲√◎繧御ｻ･螟悶・縺雁ｮ｢讒倥↓縺ｯ繝√ぉ繝・け繧､繝ｳ讖溘ｒ菴ｿ縺｣縺ｦ縺・◆縺縺上√→縺・≧菴ｿ縺・・縺代〒蝠城｡後≠繧翫∪縺帙ｓ縲ゅ・ },
  'unmanned_staff':    { label: '繧ｹ繧ｿ繝・ヵ縺ｮ莉穂ｺ九′縺ｪ縺上↑繧峨↑縺・→隱ｬ譏・, response: '縲後メ繧ｧ繝・け繧､繝ｳ謇狗ｶ壹″縺後↑縺上↑繧句・縲√せ繧ｿ繝・ヵ縺ｮ莉穂ｺ九′縺ｪ縺上↑繧九・縺ｧ縺ｯ・溘→縺泌ｿ・・縺輔ｌ繧九％縺ｨ縺後≠繧翫∪縺吶′縲・・↓繧ｹ繧ｿ繝・ヵ縺梧磁螳｢繝ｻ繧ｳ繝ｳ繧ｷ繧ｧ繝ｫ繧ｸ繝･繝ｻ貂・祉繝√ぉ繝・け縺ｪ縺ｩ莉伜刈萓｡蛟､縺ｮ鬮倥＞讌ｭ蜍吶↓髮・ｸｭ縺ｧ縺阪ｋ繧医≧縺ｫ縺ｪ繧翫∪縺吶ゅ・ },

  // 笏笏 諡・ｽ楢・ｸ榊惠 笏笏
  'person_time':       { label: '縺・▽鬆・＞繧九°遒ｺ隱阪☆繧・, response: '縲梧価遏･縺・◆縺励∪縺励◆縲ょ､ｱ遉ｼ縺・◆縺励∪縺励◆縲ゆｽ墓凾・井ｽ墓律・峨＃繧阪〒縺励◆繧画球蠖薙・謾ｯ驟堺ｺｺ讒倥→縺願ｩｱ縺ｧ縺阪∪縺吶〒縺励ｇ縺・°・溘・ },
  'person_front':      { label: '繝輔Ο繝ｳ繝医↓雉・侭騾∽ｻ倥ｒ縺企｡倥＞縺吶ｋ', response: '縲後〒縺ｯ縲√ヵ繝ｭ繝ｳ繝医・譁ｹ縺ｫ縺企｡倥＞縺励※縲∵球蠖薙・謾ｯ驟堺ｺｺ讒倥↓縺比ｸ隱ｭ縺・◆縺縺代ｋ繧医≧雉・侭繧偵Γ繝ｼ繝ｫ縺ｧ縺企√ｊ縺励※繧ゅｈ繧阪＠縺・〒縺励ｇ縺・°・溘ｈ繧阪＠縺代ｌ縺ｰ繝｡繝ｼ繝ｫ繧｢繝峨Ξ繧ｹ繧偵♀謨吶∴縺・◆縺縺代∪縺吶°・滂ｼ医ヵ繝ｭ繝ｳ繝医・譁ｹ縺ｮ縺雁錐蜑阪ｂ鬆よ斡縺ｧ縺阪∪縺吶→蟷ｸ縺・〒縺吶ゑｼ峨・ },
  'person_callback':   { label: '縺九￠逶ｴ縺励ｒ縺企｡倥＞縺吶ｋ', response: '縲後≠繧翫′縺ｨ縺・＃縺悶＞縺ｾ縺吶ゅ〒縺ｯ縲・・ｼ域凾髢灘ｸｯ・峨↓縺ゅｉ縺溘ａ縺ｦ縺企崕隧ｱ縺輔○縺ｦ縺・◆縺縺阪∪縺吶ゅｈ繧阪＠縺上♀鬘倥＞縺・◆縺励∪縺吶ゅ・ },
  'person_msg':        { label: '繝輔Ο繝ｳ繝医↓莨晁ｨ繧偵♀鬘倥＞縺吶ｋ', response: '縲後ｈ繧阪＠縺代ｌ縺ｰ縲√後ョ繝舌う繧ｹ繧ｨ繝ｼ繧ｸ繧ｧ繝ｳ繧ｷ繝ｼ縺ｮ縲・・ｈ繧翫∬・蜍輔メ繧ｧ繝・け繧､繝ｳ讖溘・縺疲｡亥・縺ｧ縺企崕隧ｱ縺後≠繧翫∪縺励◆縲阪→縺贋ｼ昴∴縺・◆縺縺代∪縺吶〒縺励ｇ縺・°・溷ｾ後⊇縺ｩ縺ゅｉ縺溘ａ縺ｦ縺秘｣邨｡縺輔○縺ｦ縺・◆縺縺阪∪縺吶ゅ・ },
  'person_name':       { label: '諡・ｽ楢・錐繧定◇縺・※縺翫￥', response: '縲後ｈ繧阪＠縺代ｌ縺ｰ縲∵球蠖薙＆繧後※縺・ｋ謾ｯ驟堺ｺｺ讒倥・縺雁錐蜑阪ｒ謨吶∴縺ｦ縺・◆縺縺代∪縺吶〒縺励ｇ縺・°・滓ｬ｡蝗槭＃騾｣邨｡縺吶ｋ髫帙↓縺雁錐蜑阪〒縺雁他縺ｳ縺ｧ縺阪∪縺吶・縺ｧ縲ゅ・ },
  'person_best_time':  { label: '譫ｶ髮ｻ縺励ｄ縺吶＞譖懈律繝ｻ譎る俣繧定◇縺・, response: '縲梧髪驟堺ｺｺ讒倥′縺企崕隧ｱ縺ｫ蜃ｺ繧・☆縺・屆譌･繧・凾髢灘ｸｯ縺ｯ縺斐＊縺・∪縺吶〒縺励ｇ縺・°・溘↑繧九∋縺上＃驛ｽ蜷医↓蜷医ｏ縺帙※縺秘｣邨｡縺励◆縺・→諤昴＞縺ｾ縺励※縲ゅ・ },

  // 笏笏 繝｡繝ｼ繝ｫ譛ｪ逹 笏笏
  'email_spam':        { label: '霑ｷ諠代Γ繝ｼ繝ｫ繧堤｢ｺ隱阪＠縺ｦ繧ゅｉ縺・, response: '縲後ｂ縺励°縺励∪縺吶→霑ｷ諠代Γ繝ｼ繝ｫ繝輔か繝ｫ繝縺ｫ蜈･縺｣縺ｦ縺・ｋ蜿ｯ閭ｽ諤ｧ縺後＃縺悶＞縺ｾ縺吶ゅ瑚ｿｷ諠代Γ繝ｼ繝ｫ縺ｧ縺ｪ縺・％縺ｨ繧貞ｱ蜻翫阪ｒ繧ｯ繝ｪ繝・け縺励※縺・◆縺縺阪∪縺吶→縲∽ｻ雁ｾ後・蜿嶺ｿ｡繝懊ャ繧ｯ繧ｹ縺ｫ螻翫￥繧医≧縺ｫ縺ｪ繧翫∪縺吶ゅ・ },
  'email_recheck':     { label: '繧｢繝峨Ξ繧ｹ繧貞・遒ｺ隱阪☆繧・, response: '縲悟ｿｵ縺ｮ縺溘ａ繝｡繝ｼ繝ｫ繧｢繝峨Ξ繧ｹ繧偵ｂ縺・ｸ蠎ｦ縺皮｢ｺ隱阪＆縺帙※縺・◆縺縺代∪縺吶〒縺励ｇ縺・°・滓ｭ｣縺励＞繧｢繝峨Ξ繧ｹ縺ｧ繧ょｱ翫°縺ｪ縺・ｴ蜷医・縲∽ｸ蠎ｦ繝輔Ο繝ｳ繝医・譁ｹ縺ｮ繧｢繝峨Ξ繧ｹ縺九ｉ蠑顔､ｾ縺ｸ騾∽ｿ｡縺励※縺・◆縺縺上→縲∽ｻ雁ｾ後せ繝繝ｼ繧ｺ縺ｫ騾∝女菫｡縺ｧ縺阪ｋ繧医≧縺ｫ縺ｪ繧翫∪縺吶ゅ・ },
  'email_resend':      { label: '縺薙■繧峨°繧牙・騾√☆繧・, response: '縲梧価遏･縺・◆縺励∪縺励◆縲ょ・蠎ｦ縺企√ｊ縺・◆縺励∪縺吶ゆｻｶ蜷阪・縲後・・ｧ倥閾ｪ蜍輔メ繧ｧ繝・け繧､繝ｳ讖溘・縺疲｡亥・縲阪〒縺企√ｊ縺励∪縺吶・縺ｧ縲√＃遒ｺ隱阪＞縺溘□縺代∪縺吶〒縺励ｇ縺・°縲ゅｂ縺怜ｱ翫°縺ｪ縺代ｌ縺ｰ縺企崕隧ｱ縺ｧ縺秘｣邨｡縺上□縺輔＞縲ゅ・ },
  'email_domain':      { label: '繝峨Γ繧､繝ｳ諡貞凄縺ｮ蜿ｯ閭ｽ諤ｧ繧呈｡亥・', response: '縲後＃蛻ｩ逕ｨ縺ｮ繝｡繝ｼ繝ｫ繧ｵ繝ｼ繝舌・縺慧eviceagency.co.jp繝峨Γ繧､繝ｳ繧呈拠蜷ｦ縺励※縺・ｋ蜿ｯ閭ｽ諤ｧ縺後＃縺悶＞縺ｾ縺吶・T諡・ｽ楢・ｧ倥↓縲掘deviceagency.co.jp縺九ｉ縺ｮ繝｡繝ｼ繝ｫ繧定ｨｱ蜿ｯ縺吶ｋ險ｭ螳壹阪ｒ縺皮｢ｺ隱阪＞縺溘□縺代∪縺吶〒縺励ｇ縺・°・溘・ },
  'email_change':      { label: '蛻･縺ｮ繧｢繝峨Ξ繧ｹ繧剃ｽｿ縺・署譯・, response: '縲後ｂ縺怜ｱ翫°縺ｪ縺・ｴ蜷医；mail縺ｪ縺ｩ蛻･縺ｮ繝｡繝ｼ繝ｫ繧｢繝峨Ξ繧ｹ繧偵♀謖√■縺ｧ縺励◆繧峨√◎縺｡繧峨↓縺企√ｊ縺吶ｋ縺薙→繧ゅ〒縺阪∪縺吶ょ倶ｺｺ繧｢繝峨Ξ繧ｹ縺ｧ繧よｧ九＞縺ｾ縺帙ｓ縲ゅ・ },

  // 笏笏 繧ｻ繝溘リ繝ｼ 笏笏
  'seminar_when':      { label: '繧ｻ繝溘リ繝ｼ譌･遞九ｒ譯亥・縺吶ｋ', response: '縲後が繝ｳ繝ｩ繧､繝ｳ繧ｻ繝溘リ繝ｼ縺ｯ豈朱ｱ豌ｴ譖懈律11譎ゅ懊・驥第屆譌･13譎ゅ憺幕蛯ｬ縺励※縺翫ｊ縺ｾ縺呻ｼ・譎る俣遞句ｺｦ繝ｻ蜿ょ刈辟｡譁呻ｼ峨ゅ＃驛ｽ蜷医↓蜷医ｏ縺帙※蛻･譌･縺ｮ縺疲｡亥・繧ょ庄閭ｽ縺ｧ縺吶・縺ｧ縲√＃蟶梧悍縺ｮ譌･譎ゅｒ縺頑蕗縺医￥縺縺輔＞縲ゅ・ },
  'seminar_content':   { label: '繧ｻ繝溘リ繝ｼ蜀・ｮｹ繧定ｪｬ譏弱☆繧・, response: '縲後そ繝溘リ繝ｼ縺ｧ縺ｯ縲∝ｮ滄圀縺ｮ謫堺ｽ懊ョ繝｢繝ｻ萓｡譬ｼ繝ｻ陬懷勧驥代・蟆主・莠倶ｾ九・PMS縺ｨ縺ｮ騾｣謳ｺ縺ｪ縺ｩ繧・譎る俣縺ｧ縺碑ｪｬ譏弱＞縺溘＠縺ｾ縺吶ょ句挨縺ｮ縺碑ｳｪ蝠上ｂ縺昴・蝣ｴ縺ｧ縺顔ｭ斐∴縺ｧ縺阪∪縺吶・oom縺ｮURL繧偵♀騾√ｊ縺・◆縺励∪縺吶・縺ｧ縲√Γ繝ｼ繝ｫ繧｢繝峨Ξ繧ｹ繧偵＞縺溘□縺代∪縺吶〒縺励ｇ縺・°・溘・ },
  'seminar_nudge':     { label: '縺ｾ縺夊ｳ・侭竊貞ｾ後〒繧ｻ繝溘リ繝ｼ謠先｡・, response: '縲後∪縺夊ｳ・侭縺縺代〒繧ゅ＃隕ｧ縺・◆縺縺阪√＃闊亥袖縺後≠繧後・繧ｻ繝溘リ繝ｼ縺ｫ繧ゅ♀豌苓ｻｽ縺ｫ縺泌盾蜉縺・◆縺縺代ｋ蠖｢縺ｧ縺・°縺後〒縺励ｇ縺・°・溯ｳ・侭繧偵♀騾√ｊ縺吶ｋ縺縺代↑繧・蛻・〒貂医∩縺ｾ縺吶ゅΓ繝ｼ繝ｫ繧｢繝峨Ξ繧ｹ繧偵＞縺溘□縺代∪縺吶°・溘・ },
  'seminar_record':    { label: '骭ｲ逕ｻ隕冶・縺ｮ謠先｡・, response: '縲後ｂ縺励そ繝溘リ繝ｼ縺ｮ譌･遞九′蜷医ｏ縺ｪ縺・ｴ蜷医・鹸逕ｻ蜍慕判繧偵♀騾√ｊ縺吶ｋ縺薙→繧ょ庄閭ｽ縺ｧ縺吶ゅ＃驛ｽ蜷医・繧医＞譎る俣縺ｫ縺碑ｦｧ縺・◆縺縺代∪縺吶ゅΓ繝ｼ繝ｫ繧｢繝峨Ξ繧ｹ繧偵＞縺溘□縺代ｌ縺ｰ莉頑律荳ｭ縺ｫ縺企√ｊ縺励∪縺吶ゅ・ },

  // 笏笏 繧､繝ｳ繝舌え繝ｳ繝・笏笏
  'inbound_lang':      { label: '螟夊ｨ隱槫ｯｾ蠢懶ｼ・3縺句嵜隱橸ｼ峨ｒ隱ｬ譏・, response: '縲悟ｼ顔､ｾ縺ｮ閾ｪ蜍輔メ繧ｧ繝・け繧､繝ｳ讖溘・13縺句嵜隱槭↓蟇ｾ蠢懊＠縺ｦ縺翫ｊ縺ｾ縺吶ょ､門嵜隱槭′闍ｦ謇九↑繧ｹ繧ｿ繝・ヵ讒倥〒繧ゅ√う繝ｳ繝舌え繝ｳ繝峨・縺雁ｮ｢讒倥↓蟇ｾ蠢懊〒縺阪∪縺吶ゅヱ繧ｹ繝昴・繝医せ繧ｭ繝｣繝ｳ繝ｻ譛ｬ莠ｺ遒ｺ隱阪ｂ繝√ぉ繝・け繧､繝ｳ讖溘〒螳檎ｵ舌＠縺ｾ縺吶ゅ・ },
  'inbound_passport':  { label: '繝代せ繝昴・繝医せ繧ｭ繝｣繝ｳ讖溯・繧定ｪｬ譏・, response: '縲後う繝ｳ繝舌え繝ｳ繝牙ｯｾ蠢懊→縺励※縲√ヱ繧ｹ繝昴・繝医せ繧ｭ繝｣繝ｳ縺ｨ鬘泌・逵滓聴蠖ｱ縺ｫ繧医ｋ譛ｬ莠ｺ遒ｺ隱肴ｩ溯・縺後＃縺悶＞縺ｾ縺吶ょ､門嵜邀阪・縺雁ｮ｢讒倥・諠・ｱ繧定・蜍輔〒蜿門ｾ励・險倬鹸縺ｧ縺阪ｋ縺溘ａ縲√ヵ繝ｭ繝ｳ繝医・謇矩俣縺悟､ｧ蟷・↓貂帙ｊ縺ｾ縺吶ゅ・ },
  'inbound_cc':        { label: '螟門嵜繧ｯ繝ｬ繧ｸ繝・ヨ繧ｫ繝ｼ繝牙ｯｾ蠢懊ｒ隱ｬ譏・, response: '縲梧ｵｷ螟也匱陦後・繧ｯ繝ｬ繧ｸ繝・ヨ繧ｫ繝ｼ繝峨ｄ髱樊磁隗ｦ豎ｺ貂茨ｼ・pple Pay繝ｻGoogle Pay遲会ｼ峨↓繧ょｯｾ蠢懊＠縺ｦ縺翫ｊ縺ｾ縺吶ゅう繝ｳ繝舌え繝ｳ繝峨・縺雁ｮ｢讒倥′繧ｹ繝繝ｼ繧ｺ縺ｫ豎ｺ貂医〒縺阪ｋ縺溘ａ縲∵髪謇輔＞繝医Λ繝悶Ν縺梧ｸ帙ｊ縺ｾ縺吶ゅ・ },
  'inbound_demand':    { label: '繧､繝ｳ繝舌え繝ｳ繝牙｢怜刈繝医Ξ繝ｳ繝峨ｒ莨昴∴繧・, response: '縲・025蟷ｴ莉･髯阪ｂ繧､繝ｳ繝舌え繝ｳ繝蛾怙隕√・蠅怜刈蛯ｾ蜷代↓縺ゅｊ縺ｾ縺吶ゆｻ翫・縺・■縺ｫ螟夊ｨ隱槫ｯｾ蠢懊・髱樊磁隗ｦ豎ｺ貂医・繝代せ繝昴・繝医せ繧ｭ繝｣繝ｳ繧呈紛蛯吶＠縺ｦ縺翫￥縺薙→縺ｧ縲∫ｫｶ蜷域命險ｭ縺ｨ縺ｮ蟾ｮ蛻･蛹悶↓縺､縺ｪ縺後ｊ縺ｾ縺吶ゅ・ },

  // 笏笏 蟆剰ｦ乗ｨ｡ 笏笏
  'size_tablet':       { label: '繧ｿ繝悶Ξ繝・ヨ蝙九ｒ謠先｡・, response: '縲悟ｰ剰ｦ乗ｨ｡譁ｽ險ｭ讒倥↓縺ｯ繧ｿ繝悶Ξ繝・ヨ蝙九′縺斐＊縺・∪縺吶ょ・譛溯ｲｻ逕ｨ縺ｯIT陬懷勧驥第ｴｻ逕ｨ縺ｧ13荳・・縲懊∵怦鬘阪・1螳､500蜀・°繧峨ゆｸ霆貞ｮｶ・医す繝ｳ繧ｰ繝ｫ繝励Λ繝ｳ・峨〒繧・9,800蜀・懊〒縺泌ｰ主・縺・◆縺縺代∪縺吶ゅ・ },
  'size_other':        { label: '繝ｫ繝ｼ繝繧ｿ繝悶Ξ繝・ヨ繝ｻ繧ｹ繝槭・繝医Ο繝・け繧呈署譯・, response: '縲碁Κ螻区焚縺悟ｰ代↑縺・命險ｭ讒倥〒繧ゅ√Ν繝ｼ繝繧ｿ繝悶Ξ繝・ヨ・亥・邱夐崕隧ｱ繝ｻ譛磯｡・螳､100蜀・懶ｼ峨ｄ繧ｯ繝ｩ繧ｦ繝峨せ繝槭・繝医Ο繝・け縺ｪ縺ｩ縲√メ繧ｧ繝・け繧､繝ｳ讖滉ｻ･螟悶・陬ｽ蜩√ｂ縺疲ｴｻ逕ｨ縺・◆縺縺代∪縺吶らｵ・∩蜷医ｏ縺帙ｋ縺薙→縺ｧ讌ｭ蜍吝柑邇・′荳翫′繧翫∪縺吶ゅ・ },
  'size_case':         { label: '蟆剰ｦ乗ｨ｡譁ｽ險ｭ縺ｮ蟆主・莠倶ｾ九ｒ謠千､ｺ', response: '縲悟ｮ溘・5螳､莉･荳九・蟆剰ｦ乗ｨ｡譌・､ｨ讒倥〒繧ょ､壽焚蟆主・縺・◆縺縺・※縺翫ｊ縺ｾ縺吶ら音縺ｫ1縲・蜷阪〒繝ｯ繝ｳ繧ｪ繝壹＆繧後※縺・ｋ譁ｽ險ｭ讒倥°繧峨・縲梧ｷｱ螟懊・繝√ぉ繝・け繧､繝ｳ蟇ｾ蠢懊′縺ｪ縺上↑繧贋ｽ薙′讌ｽ縺ｫ縺ｪ縺｣縺溘阪→縺・≧縺雁｣ｰ繧偵ｈ縺上＞縺溘□縺阪∪縺吶ゅ・ },
  'size_future':       { label: '蟆・擂縺ｮ諡｡蠑ｵ繧定ｦ玖ｶ翫＠縺ｦ謠先｡・, response: '縲御ｻ翫・蟆剰ｦ乗ｨ｡縺ｧ繧ゅ∝ｰ・擂逧・↓螳｢螳､繧貞｢励ｄ縺吩ｺ亥ｮ壹′縺ゅｌ縺ｰ縲∽ｻ翫°繧峨す繧ｹ繝・Β繧呈紛縺医※縺翫￥縺ｨ繧ｹ繝繝ｼ繧ｺ縺ｫ諡｡蠑ｵ縺ｧ縺阪∪縺吶ゅち繝悶Ξ繝・ヨ蝙九・1螳､蜊倅ｽ阪〒霑ｽ蜉縺ｧ縺阪∪縺吶・縺ｧ縲∵・髟ｷ縺ｫ蜷医ｏ縺帙※縺泌茜逕ｨ縺・◆縺縺代∪縺吶ゅ・ },

  // 笏笏 讀懆ｨ取凾譛溘〒縺ｯ縺ｪ縺・笏笏
  'timing_future':     { label: '蟆・擂縺ｮ縺溘ａ縺ｫ諠・ｱ縺縺鷹√ｋ', response: '縲梧価遏･縺・◆縺励∪縺励◆縲ゅ＃讀懆ｨ弱・譎よ悄縺ｫ縺懊・縺泌盾閠・＞縺溘□縺代ｌ縺ｰ縺ｨ諤昴＞縺ｾ縺吶・縺ｧ縲∬ｳ・侭縺縺代〒繧ゅ♀騾√ｊ縺輔○縺ｦ縺・◆縺縺代∪縺吶〒縺励ｇ縺・°・滉ｻ翫☆縺舌〒縺ｪ縺上※繧ゅ∵ュ蝣ｱ縺ｨ縺励※謖√▲縺ｦ縺翫＞縺ｦ縺・◆縺縺上□縺代〒螟ｧ荳亥､ｫ縺ｧ縺吶ゅ・ },
  'timing_task':       { label: '蜀肴楔髮ｻ繧ｿ繧ｹ繧ｯ繧定ｨｭ螳壹☆繧・, response: '縲後ｏ縺九ｊ縺ｾ縺励◆縲ゅ〒縺ｯ縲√＃讀懆ｨ弱・譎よ悄縺ｫ蜷医ｏ縺帙※縺ゅｉ縺溘ａ縺ｦ縺秘｣邨｡縺輔○縺ｦ縺・◆縺縺阪∪縺吶ゅ・・怦鬆・↓縺秘｣邨｡縺励※繧ゅｈ繧阪＠縺・〒縺励ｇ縺・°・溘・ },
  'timing_subsidy':    { label: 'IT陬懷勧驥代・譛滄剞繧剃ｼ昴∴縺ｦ蜍墓ｩ溘▼縺・, response: '縲悟ｮ溘・莉雁ｹｴ縺ｮIT陬懷勧驥代・逕ｳ隲区棧縺ｯ譌ｩ繧√↓邱繧∝・繧峨ｌ繧句庄閭ｽ諤ｧ縺後＃縺悶＞縺ｾ縺吶ゅ＃讀懆ｨ弱′蜈医↓縺ｪ繧句ｴ蜷医〒繧ゅ∬｣懷勧驥醍筏隲九□縺大・縺ｫ騾ｲ繧√※縺翫￥縺薙→縺ｧ雋ｻ逕ｨ繧貞､ｧ蟷・↓謚代∴繧峨ｌ縺ｾ縺吶・縺ｧ縲∵掠繧√↓縺皮嶌隲・＞縺溘□縺代ｋ縺ｨ蟷ｸ縺・〒縺吶ゅ・ },
  'timing_competitor': { label: '遶ｶ蜷医′蜈医↓蜍輔￥蜿ｯ閭ｽ諤ｧ繧剃ｼ昴∴繧・, response: '縲悟慍蝓溘・遶ｶ蜷医・繝・Ν讒倥′蜈医↓蟆主・縺輔ｌ繧九→縲∝哨繧ｳ繝溘ｄOTA縺ｮ隧穂ｾ｡縺ｫ蟾ｮ縺悟・繧九％縺ｨ繧ゅ＃縺悶＞縺ｾ縺吶ゅ＃讀懆ｨ取凾譛溘′譚･縺滄圀縺ｫ繧ｹ繝繝ｼ繧ｺ縺ｫ蜍輔￠繧九ｈ縺・∽ｻ翫・縺・■縺ｫ雉・侭縺縺代〒繧よ戟縺｣縺ｦ縺翫＞縺ｦ縺・◆縺縺代∪縺吶〒縺励ｇ縺・°・溘・ },
  'timing_renovation': { label: '谺｡縺ｮ謾ｹ菫ｮ繝ｻ繝ｪ繝輔か繝ｼ繝縺ｫ蜷医ｏ縺帙ｋ謠先｡・, response: '縲梧ｬ｡縺ｮ險ｭ蛯呎隼菫ｮ繧・Μ繝輔か繝ｼ繝縺ｮ繧ｿ繧､繝溘Φ繧ｰ縺ｫ蜷医ｏ縺帙※縺泌ｰ主・縺・◆縺縺乗命險ｭ讒倥ｂ螟壹＞縺ｧ縺吶ゅ◎縺ｮ繧ｿ繧､繝溘Φ繧ｰ縺ｧ縺秘｣邨｡縺・◆縺縺代ｌ縺ｰ縲∬｣懷勧驥代・譛譁ｰ諠・ｱ縺ｨ縺ｨ繧ゅ↓縺疲署譯医〒縺阪∪縺吶・縺ｧ縲∬ｳ・侭縺縺第戟縺｣縺ｦ縺翫＞縺ｦ縺・◆縺縺代∪縺吶°・溘・ },

  // 笏笏 繧ｯ繝ｬ繝ｼ繝 笏笏
  'claim_apology':     { label: '縺ｾ縺夊ｬ晉ｽｪ縺吶ｋ', response: '縲悟､ｧ螟牙､ｱ遉ｼ縺・◆縺励∪縺励◆縲ゅ＃霑ｷ諠代ｒ縺翫°縺代＠縺ｦ逕ｳ縺苓ｨｳ縺斐＊縺・∪縺帙ｓ縲ゆｻ雁ｾ後・縺秘｣邨｡繧呈而縺医＆縺帙※縺・◆縺縺阪∪縺吶ゅ≠繧翫′縺ｨ縺・＃縺悶＞縺ｾ縺励◆縲ゅ搾ｼ遺・ 譫ｶ髮ｻ繧ｯ繝ｬ繝ｼ繝縺ｫ繧ｹ繝・・繧ｸ螟画峩縺励※HubSpot縺ｫ險倬鹸縺吶ｋ・・ },
  'claim_record':      { label: 'HubSpot縺ｫ險倬鹸縺励※邨ゆｺ・, response: '・磯崕隧ｱ繧剃ｸ・㍾縺ｫ邨ゆｺ・＠縲？ubSpot縺ｮ蜿門ｼ輔せ繝・・繧ｸ繧偵梧楔髮ｻ繧ｯ繝ｬ繝ｼ繝縲阪↓螟画峩縺吶ｋ縲ゅち繧ｹ繧ｯ縺ｯ蜑企勁縲ゆｻ雁ｾ後・譫ｶ髮ｻ蟇ｾ雎｡縺九ｉ髯､螟悶☆繧九ゑｼ・ },
  'claim_freq':        { label: '譫ｶ髮ｻ鬆ｻ蠎ｦ縺ｮ隰晉ｽｪ縺ｨ鬆ｻ蠎ｦ隱ｿ謨ｴ縺ｮ謠先｡・, response: '縲後◆縺ｳ縺溘・縺秘｣邨｡縺励※縺励∪縺・､ｧ螟牙､ｱ遉ｼ縺・◆縺励∪縺励◆縲ゆｻ･蠕後・縺秘｣邨｡縺ｮ鬆ｻ蠎ｦ繧貞､ｧ蟷・↓貂帙ｉ縺吶ｈ縺・ｯｾ蠢懊＞縺溘＠縺ｾ縺吶ゅｂ縺嶺ｸ蛻・＃荳崎ｦ√〒縺励◆繧峨√◎縺ｮ譌ｨ縺翫▲縺励ｃ縺・￥縺縺輔＞縲ゆｻ雁ｾ後・荳蛻・＃騾｣邨｡繧呈而縺医＆縺帙※縺・◆縺縺阪∪縺吶ゅ・ },
}

const CATEGORY_ITEMS = [
  { id: 'cat_busy',       children: ['busy_later', 'busy_short', 'busy_task', 'busy_mail', 'busy_time_ask', 'busy_empathy'] },
  { id: 'cat_nointerest', children: ['nointerest_reason', 'nointerest_future', 'nointerest_seminar', 'nointerest_flow', 'nointerest_info', 'nointerest_subsidy', 'nointerest_competitor'] },
  { id: 'cat_other',      children: ['other_maker', 'other_compare', 'other_renewal', 'other_weakness', 'other_coexist'] },
  { id: 'cat_price',      children: ['price_subsidy', 'price_running', 'price_season', 'price_small', 'price_roi', 'price_subsidy_detail'] },
  { id: 'cat_key',        children: ['key_cylinder', 'key_smartlock', 'key_receipt', 'key_keybox', 'key_cost'] },
  { id: 'cat_custom',     children: ['custom_order', 'custom_example', 'custom_ryokan', 'custom_hospi', 'custom_demo', 'custom_ui'] },
  { id: 'cat_pms',        children: ['pms_list', 'pms_develop', 'pms_standalone', 'pms_api'] },
  { id: 'cat_unmanned',   children: ['unmanned_pr', 'unmanned_night', 'unmanned_inbound', 'unmanned_hybrid', 'unmanned_elderly', 'unmanned_staff'] },
  { id: 'cat_person',     children: ['person_time', 'person_front', 'person_callback', 'person_msg', 'person_name', 'person_best_time'] },
  { id: 'cat_email',      children: ['email_spam', 'email_recheck', 'email_resend', 'email_domain', 'email_change'] },
  { id: 'cat_seminar',    children: ['seminar_when', 'seminar_content', 'seminar_nudge', 'seminar_record'] },
  { id: 'cat_inbound',    children: ['inbound_lang', 'inbound_passport', 'inbound_cc', 'inbound_demand'] },
  { id: 'cat_size',       children: ['size_tablet', 'size_other', 'size_case', 'size_future'] },
  { id: 'cat_timing',     children: ['timing_future', 'timing_task', 'timing_subsidy', 'timing_competitor', 'timing_renovation'] },
  { id: 'cat_claim',      children: ['claim_apology', 'claim_record', 'claim_freq'] },
]

// 笏笏 繧ｭ繝ｼ繝ｯ繝ｼ繝俄・蛻・ｊ霑斐＠ID繝槭ャ繝斐Φ繧ｰ 笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏
// 逶ｸ謇九・逋ｺ險縺ｫ蜷ｫ縺ｾ繧後◎縺・↑繧ｭ繝ｼ繝ｯ繝ｼ繝峨°繧画耳螂ｨ縺吶ｋ蛻・ｊ霑斐＠ID繧定ｿ斐☆
const KEYWORD_MAP: Array<{ keywords: string[]; ids: string[] }> = [
  { keywords: ['蠢吶＠縺・, '縺・◎縺・, '莉翫・', '縺ｾ縺滉ｻ雁ｺｦ', '蠕後〒', '縺ゅ→縺ｧ', '謇九′髮｢縺・, '繧ｿ繧､繝溘Φ繧ｰ謔ｪ', '譎る俣縺ｪ縺・],
    ids: ['busy_later', 'busy_short', 'busy_task'] },
  { keywords: ['闊亥袖縺ｪ縺・, '闊亥袖縺後↑縺・, '蠢・ｦ√↑縺・, '邨先ｧ九〒縺・, '縺・ｉ縺ｪ縺・, '隕√ｉ縺ｪ縺・, '荳崎ｦ・, '繝九・繧ｺ縺後↑縺・, '閠・∴縺ｦ縺ｪ縺・],
    ids: ['nointerest_reason', 'nointerest_future', 'nointerest_info', 'nointerest_seminar'] },
  { keywords: ['莉也､ｾ', '莉悶・繝｡繝ｼ繧ｫ繝ｼ', '譌｢縺ｫ', '縺吶〒縺ｫ', '蟆主・貂医∩', '菴ｿ縺｣縺ｦ繧・, '菴ｿ縺｣縺ｦ縺・ｋ', '蜈･繧後※繧・, '蜈･繧後※縺・ｋ', '繧ゅ≧菴ｿ'],
    ids: ['other_maker', 'other_compare', 'other_renewal'] },
  { keywords: ['鬮倥＞', '縺溘°縺・, '鬮倥◎縺・, '縺企≡', '雋ｻ逕ｨ', '繧ｳ繧ｹ繝・, '莠育ｮ・, '蛟､谿ｵ', '譁咎≡', '螳峨￥縺ｪ繧・],
    ids: ['price_subsidy', 'price_running', 'price_season', 'price_small'] },
  { keywords: ['陬懷勧驥・, 'IT陬懷勧', '蜉ｩ謌・],
    ids: ['price_subsidy'] },
  { keywords: ['繧ｫ繝ｼ繝峨く繝ｼ', '繧ｫ繝ｼ繝・, '骰ｵ', '縺九℃', '繧ｷ繝ｪ繝ｳ繝繝ｼ', '迚ｩ逅・く繝ｼ', '繝峨い'],
    ids: ['key_cylinder', 'key_smartlock', 'key_receipt'] },
  { keywords: ['讌ｭ諷・, '蜷医ｏ縺ｪ縺・, '蜷医ｏ縺ｪ縺・, '縺・■縺ｫ縺ｯ', '譌・､ｨ', '豌第ｳ・, '貂ｩ豕・, '繧ｲ繧ｹ繝医ワ繧ｦ繧ｹ', '繝帙せ繝・Ν', '蟆剰ｦ乗ｨ｡', '隕乗ｨ｡縺悟ｰ上＆'],
    ids: ['custom_order', 'custom_example', 'custom_ryokan', 'size_tablet'] },
  { keywords: ['pms', 'PMS', '繝帙ユ繝ｫ繧ｷ繧ｹ繝・Β', '繧ｷ繧ｹ繝・Β騾｣謳ｺ', '莠育ｴ・す繧ｹ繝・Β', '繧ｹ繝・う繧ｷ繝ｼ', '繧ｹ繧､繝ｼ繝医ヶ繝・け', '繝吶ャ繝・],
    ids: ['pms_list', 'pms_develop'] },
  { keywords: ['辟｡莠ｺ', '繧縺倥ｓ', '繧ｹ繧ｿ繝・ヵ縺・↑縺・, '莠ｺ縺後＞縺ｪ縺・, '謗･螳｢縺ｧ縺阪↑縺・, '蟇ｾ髱｢'],
    ids: ['unmanned_pr', 'unmanned_night', 'unmanned_inbound'] },
  { keywords: ['諡・ｽ・, '縺溘ｓ縺ｨ縺・, '荳榊惠', '縺ｵ縺悶＞', '謾ｯ驟堺ｺｺ', '縺・↑縺・, '蟶ｭ繧貞､・, '縺翫ｊ縺ｾ縺帙ｓ', '蜃ｺ縺九￠'],
    ids: ['person_time', 'person_front', 'person_callback', 'person_msg'] },
  { keywords: ['繝｡繝ｼ繝ｫ', '螻翫°縺ｪ縺・, '蜿励￠蜿悶ｌ縺ｪ縺・, '霑ｷ諠・, 'spam', '譚･縺ｪ縺・, '縺薙↑縺・],
    ids: ['email_spam', 'email_recheck', 'email_resend'] },
  { keywords: ['繧ｻ繝溘リ繝ｼ', '隱ｬ譏惹ｼ・, 'zoom', 'zoom縺ｧ', '繧ｪ繝ｳ繝ｩ繧､繝ｳ', '蜿ょ刈', '譌･遞・],
    ids: ['seminar_when', 'seminar_content', 'seminar_nudge'] },
  { keywords: ['螟門嵜', '闍ｱ隱・, '荳ｭ蝗ｽ隱・, '髻灘嵜隱・, '繧､繝ｳ繝舌え繝ｳ繝・, '螟門嵜莠ｺ', '險ｪ譌･', '繝代せ繝昴・繝・, '螟夊ｨ隱・],
    ids: ['inbound_lang', 'inbound_passport'] },
  { keywords: ['蟆上＆縺・, '蟆剰ｦ乗ｨ｡', '驛ｨ螻区焚蟆・, '螳｢螳､蟆・, '荳霆貞ｮｶ', '繧ｷ繝ｳ繧ｰ繝ｫ', '謨ｰ螳､', '謨ｰ驛ｨ螻・],
    ids: ['size_tablet', 'size_other'] },
  { keywords: ['莉翫・讀懆ｨ・, '讀懆ｨ惹ｸｭ縺ｧ縺ｯ縺ｪ縺・, '譎よ悄縺ｧ縺ｯ縺ｪ縺・, '縺ｾ縺蜈・, '縺昴・縺・■', '譚･蟷ｴ', '蜀肴擂蟷ｴ', '莠育ｮ励′'],
    ids: ['timing_future', 'timing_task'] },
  { keywords: ['縺九￠繧九↑', '髮ｻ隧ｱ縺励↑縺・〒', '繧ゅ≧縺九￠', '霑ｷ諠・, '繧ｯ繝ｬ繝ｼ繝', '諤・, '縺翫％', '莠悟ｺｦ縺ｨ'],
    ids: ['claim_apology', 'claim_record'] },
]

function suggestByKeyword(input: string): string[] {
  if (!input.trim()) return []
  const lower = input.toLowerCase()
  const matched = new Map<string, number>() // id 竊・繧ｹ繧ｳ繧｢
  for (const rule of KEYWORD_MAP) {
    for (const kw of rule.keywords) {
      if (lower.includes(kw.toLowerCase())) {
        for (const id of rule.ids) {
          matched.set(id, (matched.get(id) ?? 0) + 1)
        }
      }
    }
  }
  // 繧ｹ繧ｳ繧｢鬆・↓繧ｽ繝ｼ繝医∽ｸ贋ｽ・莉ｶ縺ｾ縺ｧ
  return [...matched.entries()]
    .sort((a, b) => b[1] - a[1])
    .slice(0, 6)
    .map(([id]) => id)
}
// 笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏

type AiSuggestion = { label: string; talk: string; point: string }

const TABS = [
  { id: 'hubspot', label: '投 HubSpot謇矩・, icon: '投' },
  { id: 'script', label: '到 繝医・繧ｯ繧ｹ繧ｯ繝ｪ繝励ヨ', icon: '到' },
  { id: 'yoneyama', label: '腸 邀ｳ螻ｱ繝代ち繝ｼ繝ｳ', icon: '腸' },
  { id: 'status', label: '捷・・繧ｹ繝・・繧ｿ繧ｹ荳隕ｧ', icon: '捷・・ },
  { id: 'knowledge', label: '庁 蝠・刀遏･隴・, icon: '庁' },
  { id: 'checklist', label: '笨・繝√ぉ繝・け繝ｪ繧ｹ繝・, icon: '笨・ },
  { id: 'mail', label: '笨会ｸ・繝｡繝ｼ繝ｫ繝・Φ繝励Ξ', icon: '笨会ｸ・ },
]

export default function TeleapoPage() {
  const [activeTab, setActiveTab] = useState('hubspot')
  const [copiedKey, setCopiedKey] = useState<string | null>(null)
  const [selectedCat, setSelectedCat] = useState<string | null>(null)
  const [selectedResponse, setSelectedResponse] = useState<string | null>(null)
  const [searchInput, setSearchInput] = useState('')
  const suggestions = suggestByKeyword(searchInput)

  // 笏笏 AI 繧ｵ繧ｸ繧ｧ繧ｹ繝・(Gemini) 笏笏
  const [aiInput, setAiInput] = useState('')
  const [aiLoading, setAiLoading] = useState(false)
  const [aiSuggestions, setAiSuggestions] = useState<AiSuggestion[]>([])
  const [aiError, setAiError] = useState<string | null>(null)
  const [aiSelectedIdx, setAiSelectedIdx] = useState<number | null>(null)
  const [aiPattern, setAiPattern] = useState<'yoneyama' | 'hashimoto'>('yoneyama')

  const fetchAiSuggestions = useCallback(async (text: string, pattern: string) => {
    if (!text.trim()) return
    setAiLoading(true)
    setAiError(null)
    setAiSuggestions([])
    setAiSelectedIdx(null)
    try {
      const res = await fetch('/api/ai/teleapo-suggest', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input: text, pattern }),
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.error ?? 'API error')
      setAiSuggestions(data.suggestions ?? [])
    } catch (e) {
      setAiError(e instanceof Error ? e.message : '繧ｨ繝ｩ繝ｼ縺檎匱逕溘＠縺ｾ縺励◆')
    } finally {
      setAiLoading(false)
    }
  }, [])

  // 笏笏 邀ｳ螻ｱ繝代ち繝ｼ繝ｳ逕ｨ AI input 笏笏
  const [yoneyamaInput, setYoneyamaInput] = useState('')
  const [yoneyamaLoading, setYoneyamaLoading] = useState(false)
  const [yoneyamaSuggestions, setYoneyamaSuggestions] = useState<AiSuggestion[]>([])
  const [yoneyamaError, setYoneyamaError] = useState<string | null>(null)
  const [yoneyamaSelectedIdx, setYoneyamaSelectedIdx] = useState<number | null>(null)

  const fetchYoneyamaSuggestions = useCallback(async (text: string) => {
    if (!text.trim()) return
    setYoneyamaLoading(true)
    setYoneyamaError(null)
    setYoneyamaSuggestions([])
    setYoneyamaSelectedIdx(null)
    try {
      const res = await fetch('/api/ai/teleapo-suggest', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input: text, pattern: 'yoneyama' }),
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.error ?? 'API error')
      setYoneyamaSuggestions(data.suggestions ?? [])
    } catch (e) {
      setYoneyamaError(e instanceof Error ? e.message : '繧ｨ繝ｩ繝ｼ縺檎匱逕溘＠縺ｾ縺励◆')
    } finally {
      setYoneyamaLoading(false)
    }
  }, [])

  // 笏笏 繝｡繝｢谺・笏笏
  const MEMO_KEY = 'teleapo_memo'
  const MEMO_SAVES_KEY = 'teleapo_memo_saves'
  const [memoText, setMemoText] = useState<string>(() => {
    if (typeof window === 'undefined') return ''
    return localStorage.getItem(MEMO_KEY) ?? ''
  })
  const [savedMemos, setSavedMemos] = useState<Array<{ ts: string; text: string }>>(() => {
    if (typeof window === 'undefined') return []
    try { return JSON.parse(localStorage.getItem(MEMO_SAVES_KEY) ?? '[]') } catch { return [] }
  })
  const [memoSaved, setMemoSaved] = useState(false)
  const [memoOpen, setMemoOpen] = useState(false)

  const saveMemo = () => {
    if (!memoText.trim()) return
    localStorage.setItem(MEMO_KEY, memoText)
    const now = new Date()
    const ts = `${now.getMonth()+1}/${now.getDate()} ${String(now.getHours()).padStart(2,'0')}:${String(now.getMinutes()).padStart(2,'0')}`
    const next = [{ ts, text: memoText }, ...savedMemos].slice(0, 10) // 譛螟ｧ10莉ｶ
    setSavedMemos(next)
    localStorage.setItem(MEMO_SAVES_KEY, JSON.stringify(next))
    setMemoSaved(true)
    setTimeout(() => setMemoSaved(false), 2000)
  }

  const deleteSavedMemo = (i: number) => {
    const next = savedMemos.filter((_, idx) => idx !== i)
    setSavedMemos(next)
    localStorage.setItem(MEMO_SAVES_KEY, JSON.stringify(next))
  }

  const copy = (text: string, key: string) => {
    navigator.clipboard.writeText(text)
    setCopiedKey(key)
    setTimeout(() => setCopiedKey(null), 2000)
  }

  const selectCat = (id: string) => {
    setSelectedCat(id === selectedCat ? null : id)
    setSelectedResponse(null)
  }

  const selectResponse = (id: string) => {
    setSelectedResponse(id === selectedResponse ? null : id)
  }

  return (
    <div>
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">繝・Ξ繧｢繝・/h1>
        <p className="text-slate-400 text-sm mt-1">譬ｪ蠑丈ｼ夂､ｾ繝・ヰ繧､繧ｹ繧ｨ繝ｼ繧ｸ繧ｧ繝ｳ繧ｷ繝ｼ ・・閾ｪ蜍輔メ繧ｧ繝・け繧､繝ｳ讖・譫ｶ髮ｻ讌ｭ蜍吶・繝九Η繧｢繝ｫ</p>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 mb-6 flex-wrap">
        {TABS.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-4 py-2 rounded-xl text-sm font-medium transition-colors whitespace-nowrap ${
              activeTab === tab.id
                ? 'bg-blue-600 text-white'
                : 'bg-slate-800 text-slate-400 hover:text-white hover:bg-slate-700 border border-slate-700'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* 笏笏笏 TAB: HubSpot謇矩・笏笏笏 */}
      {activeTab === 'hubspot' && (
        <div className="space-y-6">

          {/* AI繝・Ξ繧｢繝晏ｰ主・蠕後・譁ｰ繧ｹ繝・・繧ｸ譯亥・・・026-08-12譖ｴ譁ｰ・・*/}
          <div className="bg-blue-950/40 border border-blue-700/50 rounded-2xl p-6 mb-6">
            <div className="flex items-center gap-3 mb-4">
              <span className="text-2xl">､・/span>
              <div>
                <h2 className="text-base font-bold text-white">AI繝・Ξ繧｢繝晏ｰ主・蠕後・蠖ｹ蜑ｲ蛻・球</h2>
                <p className="text-sm text-blue-300/80 mt-0.5">2026蟷ｴ8譛・2譌･譖ｴ譁ｰ / 荳肴・轤ｹ縺ｯ逕ｰ荳ｭ縺輔ｓ縺ｸ</p>
              </div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <div>
                <p className="text-sm font-bold text-green-400 mb-2">笨・縺ゅ↑縺溘′髮ｻ隧ｱ縺吶ｋ4縺､縺ｮ邂ｱ・亥━蜈磯・ｼ・/p>
                <div className="space-y-2">
                  {[
                    { num: '竭', label: 'AI繝・Ξ繧｢繝晉ｵ先棡', count: '1,237莉ｶ', desc: '骭ｲ髻ｳ繝ｻ繝｡繝｢遒ｺ隱坂・蜑榊屓縺ｮ隧ｱ繧定ｸ上∪縺医※髮ｻ隧ｱ縲よ怙繧よ・譫懊↓縺､縺ｪ縺後ｊ繧・☆縺・, color: 'green' },
                    { num: '竭｡', label: 'IVR・育ｪ∫ｴ蠕・■・・, count: '283莉ｶ', desc: '閾ｪ蜍暮浹螢ｰ縺ｧ豁｢縺ｾ縺｣縺溷・縲ゆｺｺ縺ｮ謇九〒逡ｪ蜿ｷ繧呈款縺励※遯∫ｴ縺吶ｋ', color: 'blue' },
                    { num: '竭｢', label: 'AI縺ｸ縺ｮ逹菫｡謚倥ｊ霑斐＠', count: '49莉ｶ', desc: '逶ｸ謇九°繧峨°縺代※縺阪◆竊偵☆縺宣崕隧ｱ・・, color: 'yellow' },
                    { num: '竭｣', label: '譛ｬ遉ｾ繝ｻ繝√ぉ繝ｼ繝ｳ譛ｬ驛ｨ', count: '110莉ｶ', desc: '1莉ｶ豎ｺ縺ｾ繧後・蛯倅ｸ九↓豕｢蜿翫・I縺ｧ縺ｯ遯∫ｴ荳榊庄竊剃ｺｺ縺ｮ蜉帙′蠢・ｦ・, color: 'purple' },
                  ].map((item) => (
                    <div key={item.num} className={`flex items-start gap-3 p-3 rounded-xl border ${
                      item.color === 'green' ? 'bg-green-950/40 border-green-800/40' :
                      item.color === 'blue' ? 'bg-blue-950/40 border-blue-800/40' :
                      item.color === 'yellow' ? 'bg-yellow-950/40 border-yellow-800/40' :
                      'bg-purple-950/40 border-purple-800/40'
                    }`}>
                      <span className={`text-sm font-bold flex-shrink-0 ${
                        item.color === 'green' ? 'text-green-400' :
                        item.color === 'blue' ? 'text-blue-400' :
                        item.color === 'yellow' ? 'text-yellow-400' : 'text-purple-400'
                      }`}>{item.num}</span>
                      <div>
                        <p className="text-white text-sm font-bold">{item.label} <span className="text-slate-400 font-normal">({item.count})</span></p>
                        <p className="text-slate-300 text-sm mt-0.5">{item.desc}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
              <div>
                <p className="text-sm font-bold text-slate-400 mb-2">､・AI縺梧球蠖難ｼ郁ｧｦ繧峨↑縺上※OK・・/p>
                <div className="space-y-1.5">
                  {[
                    { label: '縺薙ｌ縺九ｉ譫ｶ髮ｻ・域悴譫ｶ髮ｻ・・, count: '16,367莉ｶ', desc: 'AI縺碁・分縺ｫ縺九￠繧・ },
                    { label: 'AI繝・Ξ繧｢繝晄楔髮ｻ荳ｭ', count: '2,453莉ｶ', desc: '莉翫∪縺輔↓AI縺梧楔髮ｻ荳ｭ' },
                    { label: '逡吝ｮ育分髮ｻ隧ｱ', count: '25莉ｶ', desc: '蠕梧律AI縺後°縺醍峩縺・ },
                    { label: '髮ｻ隧ｱ荳榊・', count: '656莉ｶ', desc: '菴募ｺｦ縺九￠縺ｦ繧ょ・縺ｪ縺・・' },
                  ].map((item, i) => (
                    <div key={i} className="flex items-center gap-2 p-2 bg-slate-700/40 rounded-lg">
                      <span className="text-slate-500 text-sm">圻</span>
                      <p className="text-slate-400 text-sm">{item.label} <span className="text-slate-500">({item.count})</span> 窶・{item.desc}</p>
                    </div>
                  ))}
                </div>
                <p className="text-sm font-bold text-slate-400 mb-2 mt-3">竢ｳ 縺ゅ→縺ｧ・・邂ｱ豸亥喧蠕鯉ｼ・/p>
                <div className="space-y-1.5">
                  {[
                    { label: '繝｡繝ｫ繝槭ぎ驟堺ｿ｡・郁ｦ玖ｾｼ鬘ｧ螳｢・・, count: '208莉ｶ' },
                    { label: '蟆・擂逧・ｦ玖ｾｼ鬘ｧ螳｢', count: '142莉ｶ' },
                  ].map((item, i) => (
                    <div key={i} className="flex items-center gap-2 p-2 bg-slate-600/30 rounded-lg">
                      <span className="text-slate-500 text-sm">搭</span>
                      <p className="text-slate-400 text-sm">{item.label} <span className="text-slate-500">({item.count})</span></p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
            <div className="bg-red-950/40 border border-red-800/40 rounded-xl p-3">
              <p className="text-sm text-red-400 font-bold">笞・・驩・援・夐崕隧ｱ蠕後・蠢・★繝｡繝｢繧呈ｮ九☆縲・I繧ょ性繧∵ｬ｡縺ｮ諡・ｽ楢・′驥崎､・＠縺ｪ縺・ｈ縺・↓縲・/p>
            </div>
          </div>

          {/* 繝輔Ο繝ｼ */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
            {[
              { step: '1', title: '繝薙Η繝ｼ險ｭ螳・, desc: '繝・・繝悶Ν繝薙Η繝ｼ縺ｫ蛻・崛繝ｻ繝輔ぅ繝ｫ繧ｿ繝ｼ險ｭ螳・, color: 'blue' },
              { step: '2', title: '蛻励・邱ｨ髮・, desc: '蜑榊屓縺ｮ騾｣邨｡繝ｻ蜆ｪ蜈亥ｺｦ繧定ｿｽ蜉縺励※繧ｽ繝ｼ繝・, color: 'purple' },
              { step: '3', title: '蟇ｾ雎｡驕ｸ螳・, desc: '蜆ｪ蜈亥ｺｦ縲碁ｫ倥阪御ｸｭ縲阪・繧ｹ繧ｭ繝・・繝ｻ荳翫°繧蛾・↓', color: 'yellow' },
              { step: '4', title: '譫ｶ髮ｻ繝ｻ譖ｴ譁ｰ', desc: '諡・ｽ楢・､画峩竊帝崕隧ｱ竊偵せ繝・・繧ｸ譖ｴ譁ｰ', color: 'green' },
            ].map(item => (
              <div key={item.step} className="bg-slate-800 rounded-2xl border border-slate-700 p-5">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold mb-3 ${
                  item.color === 'blue' ? 'bg-blue-600 text-white' :
                  item.color === 'purple' ? 'bg-purple-600 text-white' :
                  item.color === 'yellow' ? 'bg-yellow-600 text-white' : 'bg-green-600 text-white'
                }`}>{item.step}</div>
                <p className="text-white font-bold text-sm mb-1">{item.title}</p>
                <p className="text-slate-400 text-xs leading-relaxed">{item.desc}</p>
              </div>
            ))}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* STEP1 */}
            <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
              <div className="flex items-center gap-3 mb-4">
                <span className="w-7 h-7 bg-blue-600 rounded-full flex items-center justify-center text-xs font-bold text-white">1</span>
                <h2 className="text-base font-bold text-white">繝薙Η繝ｼ縺ｮ險ｭ螳壹→繝輔ぅ繝ｫ繧ｿ繝ｼ</h2>
              </div>
              <div className="space-y-3">
                <div className="bg-slate-700/50 rounded-xl p-4">
                  <p className="text-sm font-bold text-blue-400 mb-2">竭 繝・・繝悶Ν繝薙Η繝ｼ縺ｫ蛻・ｊ譖ｿ縺・/p>
                  <p className="text-sm text-slate-300">HubSpot CRM 縺ｮ縲悟叙蠑輔咲判髱｢繧帝幕縺阪∬｡ｨ遉ｺ蠖｢蠑上ｒ<span className="text-blue-300 font-medium">縲後ユ繝ｼ繝悶Ν繝薙Η繝ｼ縲・/span>縺ｫ螟画峩縺吶ｋ縲・/p>
                </div>
                <div className="bg-slate-700/50 rounded-xl p-4">
                  <p className="text-sm font-bold text-blue-400 mb-2">竭｡ 隧ｳ邏ｰ繝輔ぅ繝ｫ繧ｿ繝ｼ繧定ｨｭ螳・/p>
                  <p className="text-sm text-slate-300 mb-2">縲梧･ｽ螟ｩ繝医Λ繝吶Ν・域悴譫ｶ髮ｻ・峨搾ｼ九梧球蠖楢・ｼ壽悴蜑ｲ繧雁ｽ薙※縲阪∪縺溘・縲御ｸ榊惠縲阪〒繝輔ぅ繝ｫ繧ｿ繝ｼ</p>
                  <div className="bg-slate-900 rounded-lg px-3 py-2">
                    <p className="text-yellow-300 text-sm font-medium">讌ｽ螟ｩ繝医Λ繝吶Ν・井ｸ榊惠・会ｼ医せ繝槭・繝医メ繧ｧ繝・け繧､繝ｳ・・/p>
                  </div>
                </div>
              </div>
            </div>

            {/* STEP2 */}
            <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
              <div className="flex items-center gap-3 mb-4">
                <span className="w-7 h-7 bg-purple-600 rounded-full flex items-center justify-center text-xs font-bold text-white">2</span>
                <h2 className="text-base font-bold text-white">陦ｨ遉ｺ蛻励・邱ｨ髮・→荳ｦ縺ｳ譖ｿ縺・/h2>
              </div>
              <div className="space-y-3">
                <div className="bg-slate-700/50 rounded-xl p-4">
                  <p className="text-xs text-purple-400 font-bold mb-1">竭 縲悟燕蝗槭・騾｣邨｡縲阪ｒ霑ｽ蜉</p>
                  <p className="text-sm text-slate-300">縲悟・繧堤ｷｨ髮・阪°繧峨悟燕蝗槭・騾｣邨｡縲阪ｒ讀懃ｴ｢縺励※霑ｽ蜉縲・/p>
                </div>
                <div className="bg-slate-700/50 rounded-xl p-4">
                  <p className="text-xs text-purple-400 font-bold mb-1">竭｡ 縲悟━蜈亥ｺｦ縲阪ｒ霑ｽ蜉</p>
                  <p className="text-sm text-slate-300">蜷梧ｧ倥↓縲悟━蜈亥ｺｦ縲阪ｒ霑ｽ蜉縲よ楔髮ｻ繧ｹ繧ｭ繝・・縺ｮ蛻､譁ｭ縺ｫ菴ｿ縺・・/p>
                </div>
                <div className="bg-slate-700/50 rounded-xl p-4">
                  <p className="text-xs text-purple-400 font-bold mb-1">竭｢ 縲悟燕蝗槭・騾｣邨｡縲阪〒譏・・た繝ｼ繝・/p>
                  <p className="text-sm text-slate-300">遏｢蜊ｰ繧偵け繝ｪ繝・け縺励・span className="text-white font-medium">驕主悉縺ｮ繧ゅ・縺九ｉ鬆・ｼ域・鬆・ｼ・/span>縺ｫ荳ｦ縺ｳ譖ｿ縺医・/p>
                </div>
              </div>
            </div>

            {/* STEP3 */}
            <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
              <div className="flex items-center gap-3 mb-4">
                <span className="w-7 h-7 bg-yellow-600 rounded-full flex items-center justify-center text-xs font-bold text-white">3</span>
                <h2 className="text-base font-bold text-white">譫ｶ髮ｻ蟇ｾ雎｡縺ｮ驕ｸ螳壹Ν繝ｼ繝ｫ</h2>
              </div>
              <div className="space-y-3">
                <div className="bg-red-950/50 border border-red-800/50 rounded-xl p-4">
                  <p className="text-xs text-red-400 font-bold mb-1">笞・・繧ｹ繧ｭ繝・・</p>
                  <p className="text-sm text-slate-300">蜆ｪ蜈亥ｺｦ<span className="text-red-300 font-bold">縲碁ｫ倥阪∪縺溘・縲御ｸｭ縲・/span>縺ｯ譫ｶ髮ｻ荳崎ｦ√るｲ陦御ｸｭ譯井ｻｶ縺ｮ蜿ｯ閭ｽ諤ｧ縺碁ｫ倥＞縲・/p>
                </div>
                <div className="bg-green-950/50 border border-green-800/50 rounded-xl p-4">
                  <p className="text-xs text-green-400 font-bold mb-1">笨・譫ｶ髮ｻ鬆・ｺ・/p>
                  <p className="text-sm text-slate-300">繝ｪ繧ｹ繝医・<span className="text-green-300 font-bold">荳翫°繧蛾・分</span>縺ｫ譫ｶ髮ｻ繧帝ｲ繧√ｋ縲・/p>
                </div>
                <div className="bg-slate-700/50 rounded-xl p-4">
                  <p className="text-xs text-slate-400 font-bold mb-1">庁 蜉ｹ邇・喧繝・け</p>
                  <p className="text-sm text-slate-300">繝悶Λ繧ｦ繧ｶ縺ｮ繧ｿ繝悶ｒ隍・｣ｽ縺励※縺翫￥縺ｨ縲√Μ繧ｹ繝育判髱｢縺ｨ隧ｳ邏ｰ逕ｻ髱｢繧堤ｴ譌ｩ縺剰｡後″譚･縺ｧ縺阪ｋ縲・/p>
                </div>
              </div>
            </div>

            {/* STEP4 */}
            <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
              <div className="flex items-center gap-3 mb-4">
                <span className="w-7 h-7 bg-green-600 rounded-full flex items-center justify-center text-xs font-bold text-white">4</span>
                <h2 className="text-base font-bold text-white">譫ｶ髮ｻ縺ｮ螳滓命繝輔Ο繝ｼ</h2>
              </div>
              <div className="space-y-3">
                <div className="bg-red-950/50 border border-red-800/50 rounded-xl p-4">
                  <p className="text-xs text-red-400 font-bold mb-1">笘・蠢・茨ｼ壽球蠖楢・､画峩</p>
                  <p className="text-sm text-slate-300">譫ｶ髮ｻ蜑阪↓蠢・★諡・ｽ楢・ｒ<span className="text-red-300 font-bold">縲瑚・蛻・・蜷榊燕縲・/span>縺ｫ螟画峩・・/p>
                </div>
                <div className="bg-slate-700/50 rounded-xl p-4">
                  <p className="text-xs text-green-400 font-bold mb-1">竭 髮ｻ隧ｱ繧偵°縺代ｋ</p>
                  <p className="text-sm text-slate-300">騾夊ｩｱ繝懊ち繝ｳ 竊偵碁崕隧ｱ繧偵°縺代ｋ縲阪ｒ繧ｯ繝ｪ繝・け縺励※逋ｺ菫｡縲・/p>
                </div>
                <div className="bg-slate-700/50 rounded-xl p-4">
                  <p className="text-xs text-green-400 font-bold mb-1">竭｡ 蜿門ｼ輔せ繝・・繧ｸ繧呈峩譁ｰ</p>
                  <div className="flex gap-2 flex-wrap mt-1">
                    {['讌ｽ螟ｩ繝医Λ繝吶Ν・井ｸ榊惠・・, '縺頑妙繧・, '雉・侭騾∽ｻ・, '譛ｬ遉ｾ縺ｸ', '譫ｶ髮ｻ繧ｯ繝ｬ繝ｼ繝', '莉也､ｾ陬ｽ蜩∽ｽｿ逕ｨ'].map(s => (
                      <span key={s} className="text-xs bg-slate-600/60 text-slate-300 border border-slate-500 rounded-lg px-2 py-0.5">{s}</span>
                    ))}
                  </div>
                </div>
                <div className="bg-yellow-950/50 border border-yellow-800/50 rounded-xl p-4">
                  <p className="text-xs text-yellow-400 font-bold mb-1">東 荳榊惠譎ゅ・蠢・★繧ｿ繧ｹ繧ｯ險ｭ螳・/p>
                  <p className="text-sm text-slate-300">縺・ｋ譎る俣蟶ｯ繝ｻ譌･繧定◇縺榊・縺励舌い繧ｯ繝・ぅ繝薙ユ繧｣縲鯛・縲舌ち繧ｹ繧ｯ縲代ｒ蠢・★險ｭ螳壹☆繧九％縺ｨ縲・/p>
                </div>
              </div>
            </div>
          </div>

          {/* 雉・侭騾∽ｻ倥ヵ繝ｭ繝ｼ */}
          <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
            <h2 className="text-base font-bold text-white mb-4">透 雉・侭騾∽ｻ倥↓閾ｳ縺｣縺溷ｴ蜷医・謇矩・/h2>
            <ol className="space-y-2">
              {[
                '蜿門ｼ輔・迚ｩ莉ｶ繧定｡ｨ遉ｺ竊呈ｦりｦ√°繧我ｸ九↓繧ｹ繧ｯ繝ｭ繝ｼ繝ｫ竊偵後さ繝ｳ繧ｿ繧ｯ繝医阪ｒ髢九￥',
                '繧ｳ繝ｳ繧ｿ繧ｯ繝医・繝励Ξ繝薙Η繝ｼ繧帝幕縺阪・繝｡繝ｼ繝ｫ谺・↓繧｢繝峨Ξ繧ｹ繧貞・蜉・,
                '諡・ｽ楢・・縲仙ｧ薙代↓縲後・・阪√仙錐縲代↓縲梧ｧ倥阪ｒ霑ｽ險・,
                '髮ｻ隧ｱ逡ｪ蜿ｷ縺ｮ霑ｽ蜉縺後≠繧句ｴ蜷医・縲梧声蟶ｯ逡ｪ蜿ｷ縲阪↓霑ｽ險・,
                '縲後メ繧ｧ繝・け繧､繝ｳ讖溯ｳ・侭騾∽ｻ倥阪・螳壼梛譁・ｒ繧ｳ繝斐・縺励※騾∽ｻ・,
                '雉・侭騾∽ｻ倥Γ繝ｼ繝ｫ菴懈・譎ゅ・縲先諺蜈･縲鯛・縲千ｽｲ蜷阪代〒鄂ｲ蜷阪ｒ閾ｪ蜍募・蜉・,
                '蜿門ｼ輔せ繝・・繧ｸ繧偵占ｳ・侭騾∽ｻ倥代↓螟画峩',
                '莨夂､ｾ繝励Ξ繝薙Η繝ｼ竊偵蝉ｼ夂､ｾ縺ｮ諡・ｽ楢・代↓閾ｪ蛻・・蜷榊燕繧貞・蜉・,
                '繝ｪ繝ｼ繝峨せ繝・・繧ｿ繧ｹ繧偵瑚ｳ・侭騾∽ｻ・騾ｱ髢薙阪∪縺溘・縲瑚ｳ・侭騾∽ｻ倥う繝ｳ繧ｻ繝ｳ縺ｪ縺励阪↓螟画峩',
                '繧ｿ繧ｹ繧ｯ譛滄剞繧・騾ｱ髢灘ｾ後↓險ｭ螳夲ｼ井ｻｶ蜷搾ｼ壹瑚ｳ・侭騾∽ｻ・縲・縲・搾ｼ・,
              ].map((item, i) => (
                <li key={i} className="flex gap-3 text-sm text-slate-300">
                  <span className="w-5 h-5 bg-blue-600 rounded-full flex items-center justify-center text-xs font-bold text-white flex-shrink-0 mt-0.5">{i + 1}</span>
                  {item}
                </li>
              ))}
            </ol>
            <div className="mt-4 bg-red-950/50 border border-red-800/50 rounded-xl p-3">
              <p className="text-xs text-red-400 font-bold">笞・・繧､繝ｳ繧ｻ繝ｳ譚｡莉ｶ・壼女莉倥・諡・ｽ楢・・蜷榊燕繧剃ｸ｡譁ｹ閨槭￠縺ｦ蛻昴ａ縺ｦ100蜀・ゅΓ繝｢萓具ｼ壹先球蠖灘女莉伜・縺ｫ縲・酪縲・/p>
            </div>
          </div>
        </div>
      )}

      {/* 笏笏笏 TAB: 繝医・繧ｯ繧ｹ繧ｯ繝ｪ繝励ヨ 笏笏笏 */}
      {activeTab === 'script' && (
        <div className="space-y-6">

          {/* 笏笏 蛻・ｊ霑斐＠繝翫ン 笏笏 */}
          <div className="bg-slate-800 rounded-2xl border border-blue-800/40 p-6">
            <h2 className="text-xl font-bold text-white mb-1">笞｡ 蛻・ｊ霑斐＠繝翫ン</h2>
            <p className="text-sm text-slate-400 mb-5">逶ｸ謇九・蜿榊ｿ懊ｒ繧ｯ繝ｪ繝・け 竊・蟇ｾ蠢懈婿豕輔ｒ驕ｸ縺ｶ 竊・繝医・繧ｯ縺瑚｡ｨ遉ｺ縺輔ｌ縺ｾ縺・/p>

            {/* 繧ｫ繝・ざ繝ｪ繝懊ち繝ｳ */}
            <div className="flex flex-wrap gap-3 mb-5">
              {CATEGORY_ITEMS.map(cat => (
                <button
                  key={cat.id}
                  onClick={() => selectCat(cat.id)}
                  className={`px-5 py-3 rounded-xl text-base font-bold transition-all ${
                    selectedCat === cat.id
                      ? 'bg-blue-600 text-white shadow-lg scale-105'
                      : 'bg-slate-700 text-slate-200 hover:bg-slate-600 hover:text-white border border-slate-500'
                  }`}
                >
                  {OBJECTION_TREE[cat.id]?.label}
                </button>
              ))}
            </div>

            {/* 繧ｵ繝夜∈謚・*/}
            {selectedCat && (
              <div className="border-t border-slate-700 pt-5">
                <p className="text-base text-blue-400 font-bold mb-4">縺ｩ縺・ｯｾ蠢懊＠縺ｾ縺吶°・・/p>
                <div className="flex flex-wrap gap-3 mb-5">
                  {CATEGORY_ITEMS.find(c => c.id === selectedCat)?.children.map(childId => (
                    <button
                      key={childId}
                      onClick={() => selectResponse(childId)}
                      className={`px-5 py-3 rounded-xl text-base font-bold transition-all ${
                        selectedResponse === childId
                          ? 'bg-green-600 text-white shadow-lg scale-105'
                          : 'bg-slate-700/70 text-slate-200 hover:bg-slate-600 hover:text-white border border-slate-500'
                      }`}
                    >
                      {OBJECTION_TREE[childId]?.label}
                    </button>
                  ))}
                </div>

                {/* 繝医・繧ｯ陦ｨ遉ｺ */}
                {selectedResponse && (
                  <div className="bg-green-950/60 border-2 border-green-700/70 rounded-2xl p-6">
                    <div className="flex items-center justify-between mb-3">
                      <p className="text-base text-green-400 font-bold">町 蛻・ｊ霑斐＠繝医・繧ｯ</p>
                      <button
                        onClick={() => copy(OBJECTION_TREE[selectedResponse]?.response || '', 'objection')}
                        className={`px-5 py-2 rounded-xl text-sm font-bold transition-colors ${
                          copiedKey === 'objection' ? 'bg-green-600 text-white' : 'bg-slate-700 hover:bg-slate-600 text-slate-200'
                        }`}
                      >
                        {copiedKey === 'objection' ? '笨・繧ｳ繝斐・貂医∩' : '搭 繧ｳ繝斐・'}
                      </button>
                    </div>
                    <p className="text-lg text-white leading-relaxed font-medium">
                      {OBJECTION_TREE[selectedResponse]?.response}
                    </p>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* 笏笏 邀ｳ螻ｱ繝代ち繝ｼ繝ｳ・・T陬懷勧驥題ｨｴ豎ょ梛・峨せ繧ｯ繝ｪ繝励ヨ 笏笏 */}
          <div className="bg-slate-800 rounded-2xl border border-yellow-700/40 p-6">
            <div className="flex items-center gap-3 mb-5">
              <span className="text-2xl">腸</span>
              <div>
                <h2 className="text-xl font-bold text-white">邀ｳ螻ｱ繝代ち繝ｼ繝ｳ 窶・IT陬懷勧驥題ｨｴ豎ょ梛繧ｹ繧ｯ繝ｪ繝励ヨ</h2>
                <p className="text-sm text-yellow-400/80 mt-0.5">謾ｿ蠎懊・遨肴･ｵ謾ｯ謠ｴ繝ｻ陬懷勧驥醍筏隲倶ｻ｣陦後ｒ蜑埼擇縺ｫ蜃ｺ縺励√さ繧ｹ繝磯囿螢√ｒ譛蛻昴↓蜿悶ｊ髯､縺上い繝励Ο繝ｼ繝・/p>
              </div>
            </div>
            <div className="space-y-4">

              {/* STEP 1 */}
              <div className="bg-blue-950/40 border border-blue-800/40 rounded-xl overflow-hidden">
                <div className="flex items-center justify-between px-4 pt-4 pb-2">
                  <div className="flex items-center gap-2">
                    <span className="bg-blue-700 text-white text-xs font-bold px-2 py-0.5 rounded-full">STEP 1</span>
                    <span className="text-blue-300 font-bold text-sm">蜿嶺ｻ倡ｪ∫ｴ 窶・諡・ｽ楢・↓縺､縺ｪ縺・/span>
                  </div>
                  <button onClick={() => copy(`縲後♀髮ｻ隧ｱ螟ｱ遉ｼ縺・◆縺励∪縺吶ゅョ繝舌う繧ｹ繧ｨ繝ｼ繧ｸ繧ｧ繝ｳ繧ｷ繝ｼ縺ｮ邀ｳ螻ｱ縺ｧ縺斐＊縺・∪縺吶・n繝帙ユ繝ｫ繝ｻ譌・､ｨ讒伜髄縺代・IT陬懷勧驥代・縺疲｡亥・縺ｧ縺秘｣邨｡縺励※縺・ｋ縺ｮ縺ｧ縺吶′縲―n縺疲髪驟堺ｺｺ讒倥°縲√＃諡・ｽ楢・ｧ倥・縺・ｉ縺｣縺励ｃ縺・∪縺吶〒縺励ｇ縺・°・溘港, 'ym_s1')} className={`text-xs px-3 py-1 rounded-lg font-medium transition-colors ${copiedKey === 'ym_s1' ? 'bg-green-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}>
                    {copiedKey === 'ym_s1' ? '笨・ : '搭'}
                  </button>
                </div>
                <p className="text-base text-white leading-relaxed whitespace-pre-line px-4 pb-3">{`縲後♀髮ｻ隧ｱ螟ｱ遉ｼ縺・◆縺励∪縺吶ゅョ繝舌う繧ｹ繧ｨ繝ｼ繧ｸ繧ｧ繝ｳ繧ｷ繝ｼ縺ｮ邀ｳ螻ｱ縺ｧ縺斐＊縺・∪縺吶・n繝帙ユ繝ｫ繝ｻ譌・､ｨ讒伜髄縺代・IT陬懷勧驥代・縺疲｡亥・縺ｧ縺秘｣邨｡縺励※縺・ｋ縺ｮ縺ｧ縺吶′縲―n縺疲髪驟堺ｺｺ讒倥°縲√＃諡・ｽ楢・ｧ倥・縺・ｉ縺｣縺励ｃ縺・∪縺吶〒縺励ｇ縺・°・溘港}</p>
                <div className="border-t border-blue-800/30 bg-blue-900/20 px-4 py-3">
                  <p className="text-xs text-blue-400 font-bold mb-2">楳 繝舌Μ繧ｨ繝ｼ繧ｷ繝ｧ繝ｳ</p>
                  <div className="space-y-2">
                    {[{tag:`繧ｷ繝ｳ繝励Ν迚・,text:`繝・ヰ繧､繧ｹ繧ｨ繝ｼ繧ｸ繧ｧ繝ｳ繧ｷ繝ｼ縺ｮ邀ｳ螻ｱ縺ｧ縺斐＊縺・∪縺吶・T陬懷勧驥代〒縺泌ｰ主・縺・◆縺縺代ｋ閾ｪ蜍輔メ繧ｧ繝・け繧､繝ｳ讖溘・縺疲｡亥・縺ｧ縺吶よ髪驟堺ｺｺ讒倥♀繧峨ｌ縺ｾ縺吶°・歔},
                      {tag:`譌・､ｨ蜷代￠`,text:`繝・ヰ繧､繧ｹ繧ｨ繝ｼ繧ｸ繧ｧ繝ｳ繧ｷ繝ｼ縺ｮ邀ｳ螻ｱ縺ｨ逕ｳ縺励∪縺吶よ羅鬢ｨ繝ｻ貂ｩ豕画命險ｭ讒伜髄縺代↓IT陬懷勧驥代ｒ菴ｿ縺｣縺ｦ閾ｪ蜍輔メ繧ｧ繝・け繧､繝ｳ讖溘ｒ縺泌ｰ主・縺・◆縺縺代ｋ莉ｶ縺ｧ縺秘｣邨｡縺励∪縺励◆縲ょ･ｳ蟆・＆繧薙°縺疲髪驟堺ｺｺ讒倥・縺・ｉ縺｣縺励ｃ縺・∪縺吶°・歔},
                      {tag:`繧､繝ｳ繝舌え繝ｳ繝芽ｨｴ豎Ａ,text:`繝・ヰ繧､繧ｹ繧ｨ繝ｼ繧ｸ繧ｧ繝ｳ繧ｷ繝ｼ縺ｮ邀ｳ螻ｱ縺ｧ縺斐＊縺・∪縺吶ゅう繝ｳ繝舌え繝ｳ繝牙ｯｾ蠢懊→莠ｺ謇倶ｸ崎ｶｳ縺ｮ荳｡譁ｹ繧定ｧ｣豸医〒縺阪ｋ陬懷勧驥第ｴｻ逕ｨ縺ｮ縺疲｡亥・縺ｧ縺企崕隧ｱ縺励∪縺励◆縲ゅ＃諡・ｽ薙・譁ｹ縺ｯ縺・ｉ縺｣縺励ｃ縺・∪縺吶°・歔},
                      {tag:`郢∝ｿ呎悄蜑港,text:`繝・ヰ繧､繧ｹ繧ｨ繝ｼ繧ｸ繧ｧ繝ｳ繧ｷ繝ｼ縺ｮ邀ｳ螻ｱ縺ｧ縺吶らｹ∝ｿ呎悄縺梧擂繧句燕縺ｫIT陬懷勧驥代ｒ菴ｿ縺｣縺ｦ閾ｪ蜍輔メ繧ｧ繝・け繧､繝ｳ讖溘ｒ蜈･繧後※縺・◆縺縺代ｋ縺疲｡亥・縺ｧ縺秘｣邨｡縺励∪縺励◆縲よ髪驟堺ｺｺ讒倥・縺・ｉ縺｣縺励ｃ縺・∪縺吶°・歔},
                      {tag:`謾ｿ遲冶ｨｴ豎Ａ,text:`繝・ヰ繧､繧ｹ繧ｨ繝ｼ繧ｸ繧ｧ繝ｳ繧ｷ繝ｼ縺ｮ邀ｳ螻ｱ縺ｧ縺斐＊縺・∪縺吶よ帆蠎懊′莉雁ｹｴ縺九ｉ繝帙ユ繝ｫ繝ｻ譌・､ｨ讌ｭ縺ｮ逵∽ｺｺ蛹悶ｒ驥咲せ謾ｯ謠ｴ縺励※縺翫ｊ縺ｾ縺励※縲√◎縺ｮ陬懷勧驥第ｴｻ逕ｨ縺ｮ縺疲｡亥・縺ｧ縺企崕隧ｱ縺励※縺翫ｊ縺ｾ縺吶ゅ＃諡・ｽ楢・ｧ倥・縺・ｉ縺｣縺励ｃ縺・∪縺吶°・歔}].map((v,i) => (
                      <div key={i} className="flex items-start gap-2 bg-blue-950/40 rounded-lg p-2">
                        <span className="text-xs text-blue-400 font-bold bg-blue-900/60 px-1.5 py-0.5 rounded flex-shrink-0 mt-0.5">{v.tag}</span>
                        <p className="text-sm text-slate-200 flex-1 leading-relaxed whitespace-pre-line">{v.text}</p>
                        <button onClick={() => copy(v.text, `ym_s1v${i}`)} className={`text-xs px-2 py-0.5 rounded font-medium flex-shrink-0 ${copiedKey === `ym_s1v${i}` ? 'bg-green-600 text-white' : 'bg-slate-700 text-slate-400'}`}>{copiedKey === `ym_s1v${i}` ? '笨・ : '搭'}</button>
                      </div>
                    ))}
                  </div>
                </div>
                <div className="bg-blue-900/30 px-4 py-2 border-t border-blue-800/30">
                  <p className="text-xs text-blue-300 font-bold mb-1">庁 蜿嶺ｻ倡ｪ∫ｴ縺ｮ繝昴う繝ｳ繝・/p>
                  <ul className="text-xs text-slate-300 space-y-0.5">
                    <li key={0}>繝ｻ縲栗T陬懷勧驥代・縺疲｡亥・縲阪→險縺・□縺代〒蜿嶺ｻ倥↓豁｢繧√ｉ繧後↓縺上￥縺ｪ繧具ｼ亥｣ｲ霎ｼ縺ｿ縺ｨ諤昴ｏ繧後↑縺・ｼ・/li>
                    <li key={1}>繝ｻ縲梧髪驟堺ｺｺ讒倥°諡・ｽ楢・ｧ倥阪→莠梧萱縺ｫ縺吶ｋ縺薙→縺ｧ蜷榊燕縺後↑縺上※繧ょ叙繧頑ｬ｡縺弱ｒ蠑輔″蜃ｺ縺帙ｋ</li>
                    <li key={2}>繝ｻ豁｢繧√ｉ繧後◆繧俄・縲瑚｣懷勧驥代・逕ｳ隲区悄髯舌′縺ゅｊ縺ｾ縺励※縲∵球蠖薙・譁ｹ縺ｫ荳蠎ｦ縺皮｢ｺ隱阪＞縺溘□縺代∪縺吶°縲・/li>
                    <li key={3}>繝ｻ縲御ｽ輔・縺皮畑莉ｶ縺ｧ縺吶°・溘阪→閨槭°繧後◆繧俄・縲悟嵜縺ｮIT陬懷勧驥代ｒ豢ｻ逕ｨ縺励◆閾ｪ蜍輔メ繧ｧ繝・け繧､繝ｳ讖溘・縺疲｡亥・縺ｧ縺吶・/li>
                  </ul>
                </div>
              </div>

              {/* STEP 2 */}
              <div className="bg-yellow-950/40 border border-yellow-800/40 rounded-xl overflow-hidden">
                <div className="flex items-center justify-between px-4 pt-4 pb-2">
                  <div className="flex items-center gap-2">
                    <span className="bg-yellow-700 text-white text-xs font-bold px-2 py-0.5 rounded-full">STEP 2</span>
                    <span className="text-yellow-300 font-bold text-sm">諡・ｽ楢・∈縺ｮ隨ｬ荳螢ｰ 窶・閾ｪ辟ｶ縺ｪ陬懷勧驥題ｨｴ豎・/span>
                  </div>
                  <button onClick={() => copy(`縲後≠繧翫′縺ｨ縺・＃縺悶＞縺ｾ縺吶ょｮ溘・縺・∪蝗ｽ縺ｮIT陬懷勧驥代ｒ菴ｿ縺｣縺ｦ縲―n閾ｪ蜍輔メ繧ｧ繝・け繧､繝ｳ讖溘ｒKIOSK蝙九↑繧牙ｮ溯ｳｪ48荳・・縲懊√ち繝悶Ξ繝・ヨ蝙九↑繧・3荳・・縲懊〒縺泌ｰ主・縺ｧ縺阪ｋ蛻ｶ蠎ｦ縺後≠繧翫∪縺励※縲―n陬懷勧驥代・逕ｳ隲九ｂ蠑顔､ｾ縺悟・驛ｨ莉｣陦後＠縺ｦ縺・∪縺吶ゆｻ頑律縺ｯ螢ｲ繧願ｾｼ縺ｿ縺ｧ縺ｯ縺ｪ縺上√◎縺ｮ蛻ｶ蠎ｦ縺ｮ縺疲｡亥・縺ｧ縺秘｣邨｡縺励∪縺励◆縲・n莉翫・縲・蛻・□縺代ｈ繧阪＠縺・〒縺励ｇ縺・°・溘港, 'ym_s2')} className={`text-xs px-3 py-1 rounded-lg font-medium transition-colors ${copiedKey === 'ym_s2' ? 'bg-green-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}>
                    {copiedKey === 'ym_s2' ? '笨・ : '搭'}
                  </button>
                </div>
                <p className="text-base text-white leading-relaxed whitespace-pre-line px-4 pb-3">{`縲後≠繧翫′縺ｨ縺・＃縺悶＞縺ｾ縺吶ょｮ溘・縺・∪蝗ｽ縺ｮIT陬懷勧驥代ｒ菴ｿ縺｣縺ｦ縲―n閾ｪ蜍輔メ繧ｧ繝・け繧､繝ｳ讖溘ｒKIOSK蝙九↑繧牙ｮ溯ｳｪ48荳・・縲懊√ち繝悶Ξ繝・ヨ蝙九↑繧・3荳・・縲懊〒縺泌ｰ主・縺ｧ縺阪ｋ蛻ｶ蠎ｦ縺後≠繧翫∪縺励※縲―n陬懷勧驥代・逕ｳ隲九ｂ蠑顔､ｾ縺悟・驛ｨ莉｣陦後＠縺ｦ縺・∪縺吶ゆｻ頑律縺ｯ螢ｲ繧願ｾｼ縺ｿ縺ｧ縺ｯ縺ｪ縺上√◎縺ｮ蛻ｶ蠎ｦ縺ｮ縺疲｡亥・縺ｧ縺秘｣邨｡縺励∪縺励◆縲・n莉翫・縲・蛻・□縺代ｈ繧阪＠縺・〒縺励ｇ縺・°・溘港}</p>
                <div className="border-t border-yellow-800/30 bg-yellow-900/20 px-4 py-3">
                  <p className="text-xs text-yellow-400 font-bold mb-2">楳 繝舌Μ繧ｨ繝ｼ繧ｷ繝ｧ繝ｳ</p>
                  <div className="space-y-2">
                    {[{tag:`謾ｿ蠎懊・遨肴･ｵ謾ｯ謠ｴ繧貞燕髱｢縺ｫ`,text:`謾ｿ蠎懊′莉雁ｹｴ縺九ｉ繝帙ユ繝ｫ繝ｻ譌・､ｨ讌ｭ縺ｮ逵∽ｺｺ蛹悶↓蜉帙ｒ蜈･繧後※縺・※縲！T陬懷勧驥代・莠育ｮ励ｂ縺九↑繧頑僑蜈・＆繧後※縺・ｋ繧薙〒縺吶ょｼ顔､ｾ縺檎筏隲九ｒ蜈ｨ驛ｨ繧・ｋ縺ｮ縺ｧ蠕｡遉ｾ縺ｮ縺碑ｲ諡・・縺ｻ縺ｨ繧薙←縺ｪ縺上※縲゜IOSK蝙・8荳・・縲懊〒蜈･繧後※縺・◆縺縺代∪縺吶・縲・蛻・□縺代＞縺・〒縺吶°・歔},
                      {tag:`螳溽ｸｾ蠑ｷ隱ｿ`,text:`蠑顔､ｾ縲∽ｻ雁ｹｴ縺縺代〒50譁ｽ險ｭ莉･荳翫↓IT陬懷勧驥代ｒ豢ｻ逕ｨ縺励※縺泌ｰ主・縺・◆縺縺・※縺・ｋ繧薙〒縺吶′縲∬｣懷勧驥代・蠑顔､ｾ縺悟・驛ｨ逕ｳ隲九＠縺ｾ縺吶・IOSK蝙・8荳・・縲懊√ち繝悶Ξ繝・ヨ蝙・3荳・・縲懊〒縲∝ｮ滄圀縺ｮ繧ｳ繧ｹ繝医・縺九↑繧頑椛縺医ｉ繧後∪縺吶ょｰ代＠縺縺代♀譎る俣縺・＞縺ｧ縺吶°・歔},
                      {tag:`莠ｺ謇倶ｸ崎ｶｳ繝ｻ逵∽ｺｺ蛹冶ｨｴ豎Ａ,text:`莠ｺ謇倶ｸ崎ｶｳ縺ｮ蟇ｾ遲悶→繧ｳ繧ｹ繝亥炎貂帙ｒ蜷梧凾縺ｫ縺ｧ縺阪ｋ縲！T陬懷勧驥第ｴｻ逕ｨ縺ｮ縺疲｡亥・縺ｪ繧薙〒縺吶′縲ょ嵜縺御ｻ雁ｹｴ縺九ｉ逵∽ｺｺ蛹匁兜雉・∈縺ｮ謾ｯ謠ｴ繧貞ｼｷ蛹悶＠縺ｦ縺・※縲∝ｼ顔､ｾ縺檎筏隲倶ｻ｣陦後☆繧九・縺ｧ螳溯ｳｪ雋ｻ逕ｨ繧ゅ°縺ｪ繧雁ｮ峨￥蜈･繧後ｉ繧後∪縺吶・蛻・□縺代ｈ繧阪＠縺・〒縺励ｇ縺・°・歔},
                      {tag:`繧､繝ｳ繝舌え繝ｳ繝嘉苓｣懷勧驥疏,text:`繧､繝ｳ繝舌え繝ｳ繝峨・縺雁ｮ｢讒倥・蟇ｾ蠢懊▲縺ｦ莉翫←縺・＆繧後※縺ｾ縺吶°・溷ｮ溘・IT陬懷勧驥代ｒ菴ｿ縺｣縺ｦ13縺句嵜隱槫ｯｾ蠢懊・繝√ぉ繝・け繧､繝ｳ讖溘ｒ蜈･繧後ｉ繧後ｋ蛻ｶ蠎ｦ縺後≠縺｣縺ｦ縲∬｣懷勧驥醍筏隲九・蠑顔､ｾ縺悟・驛ｨ繧・ｊ縺ｾ縺吶ょｰ代＠縺縺代♀譎る俣縺・＞縺ｧ縺吶°・歔},
                      {tag:`雋ｻ逕ｨ繧､繝ｳ繝代け繝亥・蜃ｺ縺輿,text:`蝗ｽ縺ｮ陬懷勧驥代〒閾ｪ蜍輔メ繧ｧ繝・け繧､繝ｳ讖溘′譛螳・3荳・・縺ｧ蜈･繧後ｉ繧後ｋ蛻ｶ蠎ｦ縺後≠繧九・縺ｧ縺疲｡亥・縺励※縺・ｋ繧薙〒縺吶′縲∫筏隲区焔邯壹″縺ｯ蜈ｨ驛ｨ蠑顔､ｾ縺後ｄ繧翫∪縺吶・縲・蛻・□縺代ｈ繧阪＠縺・〒縺励ｇ縺・°・歔},
                      {tag:`遶ｶ蜷亥ｷｮ蛻･蛹冒,text:`蜷後§蝨ｰ蝓溘・繝帙ユ繝ｫ讒倥′IT陬懷勧驥代〒繝√ぉ繝・け繧､繝ｳ讖溘ｒ蜈･繧悟ｧ九ａ縺ｦ縺・ｋ縺ｮ縺ｧ縺疲｡亥・縺励※縺・∪縺吶り｣懷勧驥代・逕ｳ隲九・蠑顔､ｾ縺悟・驛ｨ繧・ｊ縺ｾ縺吶＠縲゜IOSK蝙九〒48荳・・縲懊〒縺吶ょｰ代＠縺縺代＞縺・〒縺吶°・歔}].map((v,i) => (
                      <div key={i} className="flex items-start gap-2 bg-yellow-950/40 rounded-lg p-2">
                        <span className="text-xs text-yellow-400 font-bold bg-yellow-900/60 px-1.5 py-0.5 rounded flex-shrink-0 mt-0.5">{v.tag}</span>
                        <p className="text-sm text-slate-200 flex-1 leading-relaxed whitespace-pre-line">{v.text}</p>
                        <button onClick={() => copy(v.text, `ym_s2v${i}`)} className={`text-xs px-2 py-0.5 rounded font-medium flex-shrink-0 ${copiedKey === `ym_s2v${i}` ? 'bg-green-600 text-white' : 'bg-slate-700 text-slate-400'}`}>{copiedKey === `ym_s2v${i}` ? '笨・ : '搭'}</button>
                      </div>
                    ))}
                  </div>
                </div>
                <div className="bg-yellow-900/30 px-4 py-2 border-t border-yellow-800/30">
                  <p className="text-xs text-yellow-300 font-bold mb-1">庁 繝昴う繝ｳ繝・/p>
                  <ul className="text-xs text-slate-300 space-y-0.5">
                    <li key={0}>繝ｻ縲悟｣ｲ繧願ｾｼ縺ｿ縺ｧ縺ｯ縺ｪ縺上阪ｒ譏手ｨ縺吶ｋ縺縺代〒隴ｦ謌貞ｿ・′螟ｧ縺阪￥荳九′繧・/li>
                    <li key={1}>繝ｻ驥鷹｡搾ｼ・8荳・・縲・13荳・・縲懶ｼ峨ｒ蜈医↓險縺・％縺ｨ縺ｧ縲碁ｫ倥＞繧薙〒縺励ｇ縲阪→縺・≧蜈亥・隕ｳ繧帝亟縺・/li>
                    <li key={2}>繝ｻ縲瑚｣懷勧驥醍筏隲九・蠑顔､ｾ縺悟・驛ｨ繧・ｋ縲坂・蠕｡遉ｾ縺ｮ謇矩俣縺後↑縺・％縺ｨ繧貞ｼｷ隱ｿ縺吶ｋ</li>
                    <li key={3}>繝ｻ縲・縲・蛻・阪→譎る俣繧貞玄蛻・ｋ縺薙→縺ｧ縲碁聞縺上↑繧翫◎縺・阪→縺・≧譁ｭ繧雁哨螳溘ｒ貎ｰ縺・/li>
                    <li key={4}>繝ｻ縲御ｻ雁ｹｴ縺九ｉ謾ｿ蠎懊′蜉帙ｒ蜈･繧後※縺・ｋ縲坂・譎よｵ√・邱頑･諤ｧ繧貞・縺励※繧ｿ繧､繝溘Φ繧ｰ繧剃ｽ懊ｋ</li>
                  </ul>
                </div>
              </div>

              {/* STEP 3 */}
              <div className="bg-purple-950/40 border border-purple-800/40 rounded-xl overflow-hidden">
                <div className="flex items-center justify-between px-4 pt-4 pb-2">
                  <div className="flex items-center gap-2">
                    <span className="bg-purple-700 text-white text-xs font-bold px-2 py-0.5 rounded-full">STEP 3</span>
                    <span className="text-purple-300 font-bold text-sm">繝偵い繝ｪ繝ｳ繧ｰ 窶・隱ｲ鬘後ｒ閾ｪ辟ｶ縺ｫ蠑輔″蜃ｺ縺・/span>
                  </div>
                  <button onClick={() => copy(`縲梧怙霑代√≧縺｡縺ｮ蜻ｨ繧翫・繝帙ユ繝ｫ讒倥°繧峨ｂ螟憺俣縺ｮ蟇ｾ蠢懊→縺九う繝ｳ繝舌え繝ｳ繝峨・縺雁ｮ｢讒倥∈縺ｮ蟇ｾ蠢懊〒\n螟ｧ螟峨→縺・≧螢ｰ繧偵ｈ縺剰◇縺上ｓ縺ｧ縺吶′縲∝ｾ｡遉ｾ縺ｧ縺ｯ莉翫∽ｽ輔°驕狗畑縺ｧ隱ｲ鬘後↓諢溘§縺ｦ縺・ｋ縺ｨ縺薙ｍ縺ｯ縺ゅｊ縺ｾ縺吶°・溘港, 'ym_s3')} className={`text-xs px-3 py-1 rounded-lg font-medium transition-colors ${copiedKey === 'ym_s3' ? 'bg-green-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}>
                    {copiedKey === 'ym_s3' ? '笨・ : '搭'}
                  </button>
                </div>
                <p className="text-base text-white leading-relaxed whitespace-pre-line px-4 pb-3">{`縲梧怙霑代√≧縺｡縺ｮ蜻ｨ繧翫・繝帙ユ繝ｫ讒倥°繧峨ｂ螟憺俣縺ｮ蟇ｾ蠢懊→縺九う繝ｳ繝舌え繝ｳ繝峨・縺雁ｮ｢讒倥∈縺ｮ蟇ｾ蠢懊〒\n螟ｧ螟峨→縺・≧螢ｰ繧偵ｈ縺剰◇縺上ｓ縺ｧ縺吶′縲∝ｾ｡遉ｾ縺ｧ縺ｯ莉翫∽ｽ輔°驕狗畑縺ｧ隱ｲ鬘後↓諢溘§縺ｦ縺・ｋ縺ｨ縺薙ｍ縺ｯ縺ゅｊ縺ｾ縺吶°・溘港}</p>
                <div className="border-t border-purple-800/30 bg-purple-900/20 px-4 py-3">
                  <p className="text-xs text-purple-400 font-bold mb-2">楳 繝舌Μ繧ｨ繝ｼ繧ｷ繝ｧ繝ｳ</p>
                  <div className="space-y-2">
                    {[{tag:`螟憺俣迚ｹ蛹冒,text:`豺ｱ螟懊ｄ譌ｩ譛昴・繝√ぉ繝・け繧､繝ｳ縺｣縺ｦ莉翫←縺・＆繧後※縺・∪縺吶°・溷､憺俣繧ｹ繧ｿ繝・ヵ縺ｮ繧ｳ繧ｹ繝医ｄ縲∝ｯｾ蠢懆ｲ諡・↓縺､縺・※菴輔°隱ｲ鬘後・縺ゅｊ縺ｾ縺吶°・歔},
                      {tag:`繧､繝ｳ繝舌え繝ｳ繝臥音蛹冒,text:`譛霑代う繝ｳ繝舌え繝ｳ繝峨・縺雁ｮ｢讒倥・蠅励∴縺ｦ縺阪※縺・∪縺吶°・溷､門嵜隱槭・蟇ｾ蠢懊→縺九√ヱ繧ｹ繝昴・繝医・遒ｺ隱阪→縺九▲縺ｦ謇矩俣縺ｫ縺ｪ縺｣縺ｦ縺・∪縺帙ｓ縺具ｼ歔},
                      {tag:`莠ｺ謇倶ｸ崎ｶｳ迚ｹ蛹冒,text:`譛霑代せ繧ｿ繝・ヵ縺ｮ謗｡逕ｨ縺｣縺ｦ鬆・ｪｿ縺ｧ縺吶°・滓･ｭ逡悟・菴薙〒莠ｺ謇倶ｸ崎ｶｳ縺ｨ縺・≧隧ｱ繧定◇縺上％縺ｨ縺悟､壹￥縺ｦ縲ゅΡ繝ｳ繧ｪ繝壹→縺狗ｹ∝ｿ呎悄縺ｮ蟇ｾ蠢懊→縺句､ｧ螟峨§繧・↑縺・°縺ｪ縺ｨ諤昴▲縺ｦ縲Ａ},
                      {tag:`繧ｳ繧ｹ繝郁ｨｴ豎Ａ,text:`郢∝ｿ呎悄縺ｨ髢第淵譛溘〒莠ｺ莉ｶ雋ｻ縺ｮ蟾ｮ縺悟､ｧ縺阪＞縺｣縺ｦ譁ｽ險ｭ縺輔ｓ螟壹＞繧薙〒縺吶′縲∝ｾ｡遉ｾ縺ｯ縺ｩ縺・〒縺吶°・溽ｹ∝ｿ呎悄縺縺台ｽｿ縺医ｋ繝励Λ繝ｳ繧ゅ≠繧九・縺ｧ蜿り・↓縺ｪ繧九°縺ｪ縺ｨ諤昴▲縺ｦ縲Ａ},
                      {tag:`PMS繝ｻ騾｣謳ｺ`,text:`莉翫←繧薙↑繝帙ユ繝ｫ繧ｷ繧ｹ繝・Β・・MS・峨ｒ縺贋ｽｿ縺・〒縺吶°・溘メ繧ｧ繝・け繧､繝ｳ讖溘→縺ｮ騾｣謳ｺ縺後〒縺阪ｋ縺ｨ驕狗畑縺後°縺ｪ繧翫せ繝繝ｼ繧ｺ縺ｫ縺ｪ繧九・縺ｧ縲∽ｽｿ縺｣縺ｦ縺・ｋ繧ｷ繧ｹ繝・Β繧定◇縺九○縺ｦ繧ゅｉ縺医∪縺吶°・歔},
                      {tag:`險ｭ蛯呎峩譁ｰ繧ｿ繧､繝溘Φ繧ｰ`,text:`莉翫♀菴ｿ縺・・繝輔Ο繝ｳ繝郁ｨｭ蛯吶▲縺ｦ縺・▽鬆・＃蟆主・縺輔ｌ縺溘ｂ縺ｮ縺ｧ縺吶°・櫑T陬懷勧驥代・繧ｿ繧､繝溘Φ繧ｰ縺ｨ譖ｴ譁ｰ譎よ悄縺悟粋縺・→雋ｻ逕ｨ縺後°縺ｪ繧頑椛縺医ｉ繧後ｋ縺ｮ縺ｧ閨槭°縺帙※繧ゅｉ縺医∪縺吶°・歔}].map((v,i) => (
                      <div key={i} className="flex items-start gap-2 bg-purple-950/40 rounded-lg p-2">
                        <span className="text-xs text-purple-400 font-bold bg-purple-900/60 px-1.5 py-0.5 rounded flex-shrink-0 mt-0.5">{v.tag}</span>
                        <p className="text-sm text-slate-200 flex-1 leading-relaxed whitespace-pre-line">{v.text}</p>
                        <button onClick={() => copy(v.text, `ym_s3v${i}`)} className={`text-xs px-2 py-0.5 rounded font-medium flex-shrink-0 ${copiedKey === `ym_s3v${i}` ? 'bg-green-600 text-white' : 'bg-slate-700 text-slate-400'}`}>{copiedKey === `ym_s3v${i}` ? '笨・ : '搭'}</button>
                      </div>
                    ))}
                  </div>
                </div>
                <div className="bg-purple-900/30 px-4 py-2 border-t border-purple-800/30">
                  <p className="text-xs text-purple-300 font-bold mb-1">庁 繝偵い繝ｪ繝ｳ繧ｰ縺ｮ繝昴う繝ｳ繝・/p>
                  <ul className="text-xs text-slate-300 space-y-0.5 mb-2">
                    <li key={0}>繝ｻ縲梧怙霑代ｈ縺剰◇縺上ｓ縺ｧ縺吶′縲坂・蜷梧･ｭ莉也､ｾ縺ｮ迥ｶ豕√ｒ莨昴∴繧九％縺ｨ縺ｧ螳牙ｿ・─縺ｨ蜈ｱ諢溘ｒ蠑輔″蜃ｺ縺・/li>
                    <li key={1}>繝ｻ蜈ｷ菴謎ｾ具ｼ亥､憺俣蟇ｾ蠢懊・繧､繝ｳ繝舌え繝ｳ繝臥ｭ会ｼ峨ｒ蜃ｺ縺吶％縺ｨ縺ｧ縲後≧縺｡縺ｯ螟ｧ荳亥､ｫ縲阪°縲後◎縺・↑繧薙〒縺吶阪°繧貞ｼ輔″蜃ｺ縺励ｄ縺吶￥縺ｪ繧・/li>
                    <li key={2}>繝ｻ隱ｲ鬘後′蜃ｺ縺溘ｉ竊偵悟ｮ溘・縺昴ｌ縲！T陬懷勧驥代〒隗｣豎ｺ縺輔ｌ縺ｦ縺・ｋ繝帙ユ繝ｫ讒倥・莠倶ｾ九′縺ゅｊ縺ｾ縺吶阪↓縺､縺ｪ縺・/li>
                    <li key={3}>繝ｻ隱ｲ鬘後′縺ｪ縺代ｌ縺ｰ竊偵後〒縺励◆繧画ュ蝣ｱ縺縺醍ｽｮ縺九○縺ｦ縺・◆縺縺代ｌ縺ｰ縲阪→繝｡繝ｼ繝ｫ騾∽ｻ倥↓蛻・ｊ譖ｿ縺医ｋ</li>
                  </ul>
                  <p className="text-xs text-purple-300 font-bold mb-1">諡ｾ縺・∋縺阪く繝ｼ繝ｯ繝ｼ繝・/p>
                  <div className="flex flex-wrap gap-1.5">
                    <span key='螟憺俣蟇ｾ蠢・ className="text-xs bg-purple-900/60 text-purple-200 border border-purple-700/50 rounded-lg px-2 py-0.5">螟憺俣蟇ｾ蠢・/span>
                    <span key='骰ｵ貂｡縺励・謇矩俣' className="text-xs bg-purple-900/60 text-purple-200 border border-purple-700/50 rounded-lg px-2 py-0.5">骰ｵ貂｡縺励・謇矩俣</span>
                    <span key='繧､繝ｳ繝舌え繝ｳ繝・ className="text-xs bg-purple-900/60 text-purple-200 border border-purple-700/50 rounded-lg px-2 py-0.5">繧､繝ｳ繝舌え繝ｳ繝・/span>
                    <span key='螟夊ｨ隱槫ｯｾ蠢・ className="text-xs bg-purple-900/60 text-purple-200 border border-purple-700/50 rounded-lg px-2 py-0.5">螟夊ｨ隱槫ｯｾ蠢・/span>
                    <span key='繧ｹ繧ｿ繝・ヵ荳崎ｶｳ' className="text-xs bg-purple-900/60 text-purple-200 border border-purple-700/50 rounded-lg px-2 py-0.5">繧ｹ繧ｿ繝・ヵ荳崎ｶｳ</span>
                    <span key='繝ｯ繝ｳ繧ｪ繝・ className="text-xs bg-purple-900/60 text-purple-200 border border-purple-700/50 rounded-lg px-2 py-0.5">繝ｯ繝ｳ繧ｪ繝・/span>
                    <span key='郢∝ｿ呎悄' className="text-xs bg-purple-900/60 text-purple-200 border border-purple-700/50 rounded-lg px-2 py-0.5">郢∝ｿ呎悄</span>
                    <span key='邊ｾ邂励Α繧ｹ' className="text-xs bg-purple-900/60 text-purple-200 border border-purple-700/50 rounded-lg px-2 py-0.5">邊ｾ邂励Α繧ｹ</span>
                    <span key='莠ｺ莉ｶ雋ｻ' className="text-xs bg-purple-900/60 text-purple-200 border border-purple-700/50 rounded-lg px-2 py-0.5">莠ｺ莉ｶ雋ｻ</span>
                    <span key='PMS騾｣謳ｺ' className="text-xs bg-purple-900/60 text-purple-200 border border-purple-700/50 rounded-lg px-2 py-0.5">PMS騾｣謳ｺ</span>
                    <span key='險ｭ蛯呵∵愎蛹・ className="text-xs bg-purple-900/60 text-purple-200 border border-purple-700/50 rounded-lg px-2 py-0.5">險ｭ蛯呵∵愎蛹・/span>
                    <span key='豺ｱ螟懷ｸｯ' className="text-xs bg-purple-900/60 text-purple-200 border border-purple-700/50 rounded-lg px-2 py-0.5">豺ｱ螟懷ｸｯ</span>
                  </div>
                </div>
              </div>

              {/* STEP 4 YES */}
              <div className="bg-green-950/40 border border-green-800/40 rounded-xl overflow-hidden">
                <div className="flex items-center justify-between px-4 pt-4 pb-2">
                  <div className="flex items-center gap-2">
                    <span className="bg-green-700 text-white text-xs font-bold px-2 py-0.5 rounded-full">STEP 4</span>
                    <span className="text-green-300 font-bold text-sm">隱ｲ鬘後≠繧・竊・莠倶ｾ区署譯・竊・繧｢繝晏叙繧・/span>
                  </div>
                  <button onClick={() => copy(`縲後◎縺・〒縺吶ｈ縺ｭ縲ょｮ溘・縲√◎縺ｮ隱ｲ鬘後ｒIT陬懷勧驥代ｒ菴ｿ縺｣縺ｦ縺・∪縺剰ｧ｣豎ｺ縺輔ｌ縺ｦ縺・ｋ繝帙ユ繝ｫ讒倥・莠倶ｾ九′謇句・縺ｫ縺ゅｊ縺ｾ縺吶・n雉・侭縺ｨ陬懷勧驥代・逕ｳ隲九せ繧ｱ繧ｸ繝･繝ｼ繝ｫ繧偵Γ繝ｼ繝ｫ縺ｧ縺企√ｊ縺励※繧ゅ＞縺・〒縺吶°・歃n縺昴・蠕後・5蛻・□縺代＞縺溘□縺・※縲∬｣懷勧驥代ｒ菴ｿ縺｣縺溷・菴鍋噪縺ｪ縺碑ｪｬ譏弱′縺ｧ縺阪ｌ縺ｰ縺ｨ諤昴＞縺ｾ縺励※縲ゅ港, 'ym_s4y')} className={`text-xs px-3 py-1 rounded-lg font-medium transition-colors ${copiedKey === 'ym_s4y' ? 'bg-green-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}>
                    {copiedKey === 'ym_s4y' ? '笨・ : '搭'}
                  </button>
                </div>
                <p className="text-base text-white leading-relaxed whitespace-pre-line px-4 pb-3">{`縲後◎縺・〒縺吶ｈ縺ｭ縲ょｮ溘・縲√◎縺ｮ隱ｲ鬘後ｒIT陬懷勧驥代ｒ菴ｿ縺｣縺ｦ縺・∪縺剰ｧ｣豎ｺ縺輔ｌ縺ｦ縺・ｋ繝帙ユ繝ｫ讒倥・莠倶ｾ九′謇句・縺ｫ縺ゅｊ縺ｾ縺吶・n雉・侭縺ｨ陬懷勧驥代・逕ｳ隲九せ繧ｱ繧ｸ繝･繝ｼ繝ｫ繧偵Γ繝ｼ繝ｫ縺ｧ縺企√ｊ縺励※繧ゅ＞縺・〒縺吶°・歃n縺昴・蠕後・5蛻・□縺代＞縺溘□縺・※縲∬｣懷勧驥代ｒ菴ｿ縺｣縺溷・菴鍋噪縺ｪ縺碑ｪｬ譏弱′縺ｧ縺阪ｌ縺ｰ縺ｨ諤昴＞縺ｾ縺励※縲ゅ港}</p>
                <div className="border-t border-green-800/30 bg-green-900/20 px-4 py-3">
                  <p className="text-xs text-green-400 font-bold mb-2">楳 繝舌Μ繧ｨ繝ｼ繧ｷ繝ｧ繝ｳ・医い繝晏叙繧翫ヱ繧ｿ繝ｼ繝ｳ・・/p>
                  <div className="space-y-2">
                    {[{tag:`Zoom謠先｡・,text:`雉・侭騾√▲縺溘≠縺ｨ縺ｧ縲〇oom縺ｧ15蛻・⊇縺ｩ縺碑ｪｬ譏弱〒縺阪ｌ縺ｰ荳逡ｪ繧上°繧翫ｄ縺吶＞縺ｨ諤昴≧繧薙〒縺吶′縲∵擂騾ｱ縺ｮ轣ｫ譖懊°豌ｴ譖懊←縺｡繧峨°縺秘・蜷医ｈ縺・〒縺吶°・歔},
                      {tag:`繧ｻ繝溘リ繝ｼ隱伜ｰ餐,text:`豈朱ｱ豌ｴ譖・1譎ゅ・驥第屆13譎ゅ↓繧ｪ繝ｳ繝ｩ繧､繝ｳ縺ｮ繧ｻ繝溘リ繝ｼ繧偵ｄ縺｣縺ｦ縺・∪縺励※縲∬｣懷勧驥代・逕ｳ隲九・隧ｱ繧・ｮ滄圀縺ｮ謫堺ｽ懊ｂ隕九※縺・◆縺縺代∪縺吶ら┌譁吶〒縺吶＠縲√＞縺九′縺ｧ縺吶°・歔},
                      {tag:`險ｪ蝠乗署譯・,text:`繧ゅ＠繧医￠繧後・螳滄圀縺ｫ陬ｽ蜩√ｒ隕九※縺・◆縺縺阪↑縺後ｉ縺碑ｪｬ譏弱〒縺阪ｌ縺ｰ縺ｨ諤昴≧縺ｮ縺ｧ縺吶′縲∵擂騾ｱ縺秘・蜷医・繧医＞譌･縺ｯ縺ゅｊ縺ｾ縺吶°・歔},
                      {tag:`雉・侭縺ｮ縺ｿ・医た繝輔ヨ・荏,text:`縺ｾ縺夊ｳ・侭縺縺鷹√ｊ縺ｾ縺吶・縲り｣懷勧驥代・逕ｳ隲九せ繧ｱ繧ｸ繝･繝ｼ繝ｫ縺ｨ蟆主・莠倶ｾ九ｂ蜈･縺｣縺ｦ縺・∪縺吶ゅΓ繝ｼ繝ｫ繧｢繝峨Ξ繧ｹ繧呈蕗縺医※繧ゅｉ縺医∪縺吶°・歔},
                      {tag:`譛滄剞險ｴ豎ゅ〒繧｢繝拜,text:`陬懷勧驥代・逕ｳ隲区棧縺梧掠繧√↓邱繧∝・繧峨ｌ繧九％縺ｨ繧ゅ≠繧九・縺ｧ縲∵掠繧√↓蜍輔＞縺滓婿縺後＞縺・命險ｭ讒倥ｂ螟壹＞繧薙〒縺吶よ擂騾ｱ15蛻・□縺代♀譎る俣繧ゅｉ縺医∪縺帙ｓ縺具ｼ歔},
                      {tag:`莠倶ｾ九〒蠑輔″蟇・○`,text:`蠕｡遉ｾ縺ｨ莨ｼ縺溯ｦ乗ｨ｡縺ｮ繝帙ユ繝ｫ讒倥′陬懷勧驥代ｒ菴ｿ縺｣縺ｦ蜈･繧後◆莠倶ｾ九′縺ゅｋ縺ｮ縺ｧ縲√◎縺ｮ隧ｱ縺縺代〒繧ゅ♀莨昴∴縺ｧ縺阪ｌ縺ｰ縲・5蛻・□縺岨oom縺ｧ縺・°縺後〒縺吶°・歔}].map((v,i) => (
                      <div key={i} className="flex items-start gap-2 bg-green-950/40 rounded-lg p-2">
                        <span className="text-xs text-green-400 font-bold bg-green-900/60 px-1.5 py-0.5 rounded flex-shrink-0 mt-0.5">{v.tag}</span>
                        <p className="text-sm text-slate-200 flex-1 leading-relaxed whitespace-pre-line">{v.text}</p>
                        <button onClick={() => copy(v.text, `ym_s4v${i}`)} className={`text-xs px-2 py-0.5 rounded font-medium flex-shrink-0 ${copiedKey === `ym_s4v${i}` ? 'bg-green-600 text-white' : 'bg-slate-700 text-slate-400'}`}>{copiedKey === `ym_s4v${i}` ? '笨・ : '搭'}</button>
                      </div>
                    ))}
                  </div>
                </div>
                <div className="bg-green-900/30 px-4 py-2 border-t border-green-800/30">
                  <p className="text-xs text-green-300 font-bold mb-1">庁 繧｢繝晉佐蠕励・繧ｳ繝・/p>
                  <ul className="text-xs text-slate-300 space-y-0.5">
                    <li key={0}>繝ｻ縲瑚ｳ・侭繧帝√ｋ縲坂・縲・5蛻・□縺代阪・2谿ｵ髫弱〒繧｢繝昴・繝上・繝峨Ν繧剃ｸ九￡繧・/li>
                    <li key={1}>繝ｻ譌･遞九・縲梧擂騾ｱ縺ｮ轣ｫ譖懊°豌ｴ譖懊√←縺｡繧峨′縺秘・蜷医ｈ縺・〒縺吶°・溘阪→莠梧萱縺ｧ閨槭￥</li>
                    <li key={2}>繝ｻZoom縺ｧ繧ょ庄縺ｨ莨昴∴繧後・蝨ｰ譁ｹ縺ｮ繝帙ユ繝ｫ繧ょｯｾ蠢懊〒縺阪ｋ</li>
                    <li key={3}>繝ｻ縲瑚｣懷勧驥代・逕ｳ隲区悄髯舌′縺ゅｋ縲坂・邱頑･諤ｧ繧貞・縺励※繧｢繝晄律遞九ｒ譌ｩ繧√ｋ</li>
                  </ul>
                </div>
              </div>

              {/* STEP 4' NO */}
              <div className="bg-slate-700/50 border border-slate-600/40 rounded-xl overflow-hidden">
                <div className="flex items-center justify-between px-4 pt-4 pb-2">
                  <div className="flex items-center gap-2">
                    <span className="bg-slate-600 text-white text-xs font-bold px-2 py-0.5 rounded-full">STEP 4&apos;</span>
                    <span className="text-slate-300 font-bold text-sm">隱ｲ鬘後↑縺・竊・諠・ｱ縺縺醍ｽｮ縺・※谺｡縺ｫ縺､縺ｪ縺・/span>
                  </div>
                  <button onClick={() => copy(`縲後◎縺・〒縺吶°縲・T陬懷勧驥代▲縺ｦ豈主ｹｴ逕ｳ隲区棧縺後≠繧九・縺ｧ縲√ち繧､繝溘Φ繧ｰ縺梧擂縺溘→縺阪・縺溘ａ縺ｫ諠・ｱ縺縺第戟縺｣縺ｦ縺翫＞縺ｦ繧ゅｉ縺医ｌ縺ｰ蜊∝・縺ｧ縺吶・n陬懷勧驥代・讎りｦ√→陬ｽ蜩√・雉・侭繧偵Γ繝ｼ繝ｫ縺ｧ縺企√ｊ縺励※繧ゅ＞縺・〒縺吶°・歃n繝｡繝ｼ繝ｫ繧｢繝峨Ξ繧ｹ繧偵＞縺溘□縺代ｌ縺ｰ莉頑律荳ｭ縺ｫ騾√ｊ縺ｾ縺吶ゅ港, 'ym_s4n')} className={`text-xs px-3 py-1 rounded-lg font-medium transition-colors ${copiedKey === 'ym_s4n' ? 'bg-green-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}>
                    {copiedKey === 'ym_s4n' ? '笨・ : '搭'}
                  </button>
                </div>
                <p className="text-base text-white leading-relaxed whitespace-pre-line px-4 pb-3">{`縲後◎縺・〒縺吶°縲・T陬懷勧驥代▲縺ｦ豈主ｹｴ逕ｳ隲区棧縺後≠繧九・縺ｧ縲√ち繧､繝溘Φ繧ｰ縺梧擂縺溘→縺阪・縺溘ａ縺ｫ諠・ｱ縺縺第戟縺｣縺ｦ縺翫＞縺ｦ繧ゅｉ縺医ｌ縺ｰ蜊∝・縺ｧ縺吶・n陬懷勧驥代・讎りｦ√→陬ｽ蜩√・雉・侭繧偵Γ繝ｼ繝ｫ縺ｧ縺企√ｊ縺励※繧ゅ＞縺・〒縺吶°・歃n繝｡繝ｼ繝ｫ繧｢繝峨Ξ繧ｹ繧偵＞縺溘□縺代ｌ縺ｰ莉頑律荳ｭ縺ｫ騾√ｊ縺ｾ縺吶ゅ港}</p>
                <div className="border-t border-slate-600/30 bg-slate-600/20 px-4 py-3">
                  <p className="text-xs text-slate-400 font-bold mb-2">楳 繝舌Μ繧ｨ繝ｼ繧ｷ繝ｧ繝ｳ</p>
                  <div className="space-y-2">
                    {[{tag:`陬懷勧驥第悄髯舌ｒ菴ｿ縺・,text:`莉雁ｹｴ縺ｮIT陬懷勧驥代・逕ｳ隲区悄髯舌′霑代▼縺・※縺阪※縺・ｋ縺ｮ縺ｧ縲∵ュ蝣ｱ縺縺代〒繧よ戟縺｣縺ｦ縺翫＞縺ｦ繧ゅｉ縺医ｋ縺ｨ縲√ち繧､繝溘Φ繧ｰ縺梧擂縺溘→縺阪↓縺吶＄蜍輔￠縺ｾ縺吶ゅΓ繝ｼ繝ｫ繧｢繝峨Ξ繧ｹ縺縺第蕗縺医※縺・◆縺縺代∪縺吶°・歔},
                      {tag:`遶ｶ蜷域命險ｭ繧剃ｽｿ縺・,text:`蜷後§蝨ｰ蝓溘・繝帙ユ繝ｫ讒倥′繧ゅ≧蜈･繧悟ｧ九ａ縺ｦ縺・ｋ縺ｮ縺ｧ縲∝哨繧ｳ繝溘・隧穂ｾ｡縺ｫ蟾ｮ縺悟・繧句燕縺ｫ諠・ｱ縺縺代〒繧よ戟縺｣縺ｦ縺翫＞縺ｦ繧ゅｉ縺医ｌ縺ｰ縲ゆｻ頑律荳ｭ縺ｫ繝｡繝ｼ繝ｫ縺ｧ騾√ｊ縺ｾ縺吶・縲Ａ},
                      {tag:`郢∝ｿ呎悄蜑阪ｒ菴ｿ縺・,text:`谺｡縺ｮ郢∝ｿ呎悄縺梧擂繧句燕縺ｫ蜍輔￠縺ｰ陬懷勧驥代ｂ髢薙↓蜷医＞縺ｾ縺吶・縺ｧ縲∽ｻ頑律縺ｯ雉・侭縺縺鷹√ｉ縺帙※縺上□縺輔＞縲ゅΓ繝ｼ繝ｫ繧｢繝峨Ξ繧ｹ繧呈蕗縺医※繧ゅｉ縺医∪縺吶°・歔},
                      {tag:`謾ｿ蠎懊・譁ｹ驥昴ｒ菴ｿ縺・,text:`謾ｿ蠎懊′莉雁ｹｴ縺九ｉ繝帙ユ繝ｫ繝ｻ譌・､ｨ讌ｭ縺ｸ縺ｮ逵∽ｺｺ蛹匁髪謠ｴ繧貞ｼｷ蛹悶＠縺ｦ縺・∪縺吶・縺ｧ縲∵擂蟷ｴ莉･髯阪ｂ陬懷勧驥代・譫縺ｯ邯壹￥莠亥ｮ壹〒縺吶よュ蝣ｱ縺縺第戟縺｣縺ｦ縺翫＞縺ｦ繧ゅｉ縺医ｋ縺ｨ蠕後〒蠖ｹ縺ｫ遶九■縺ｾ縺吶Ａ},
                      {tag:`繝励Ξ繝・す繝｣繝ｼ縺ｪ縺汁,text:`繧上°繧翫∪縺励◆縲ら┌逅・↓莉翫☆縺先ｱｺ繧√※繧ゅｉ縺翫≧縺ｨ縺ｯ諤昴▲縺ｦ縺・↑縺・・縺ｧ縲∬ｳ・侭縺縺鷹√ｊ縺ｾ縺吶ゅΓ繝ｼ繝ｫ繧｢繝峨Ξ繧ｹ縺縺代＞縺溘□縺代ｌ縺ｰ螟ｧ荳亥､ｫ縺ｧ縺吶Ａ}].map((v,i) => (
                      <div key={i} className="flex items-start gap-2 bg-slate-700/50 rounded-lg p-2">
                        <span className="text-xs text-slate-300 font-bold bg-slate-600/80 px-1.5 py-0.5 rounded flex-shrink-0 mt-0.5">{v.tag}</span>
                        <p className="text-sm text-slate-200 flex-1 leading-relaxed whitespace-pre-line">{v.text}</p>
                        <button onClick={() => copy(v.text, `ym_s4nv${i}`)} className={`text-xs px-2 py-0.5 rounded font-medium flex-shrink-0 ${copiedKey === `ym_s4nv${i}` ? 'bg-green-600 text-white' : 'bg-slate-700 text-slate-400'}`}>{copiedKey === `ym_s4nv${i}` ? '笨・ : '搭'}</button>
                      </div>
                    ))}
                  </div>
                </div>
                <div className="bg-slate-600/30 px-4 py-2 border-t border-slate-600/30">
                  <p className="text-xs text-slate-400 font-bold mb-1">庁 繝昴う繝ｳ繝・/p>
                  <ul className="text-xs text-slate-400 space-y-0.5">
                    <li key={0}>繝ｻ縲瑚ｳ・侭騾∽ｻ・竊・3騾ｱ髢謎ｻ･蜀・↓蜀肴楔髮ｻ縲阪〒繧､繝ｳ繧ｻ繝ｳ繝・ぅ繝門ｯｾ雎｡繧堤漁縺・/li>
                    <li key={1}>繝ｻ繝｡繧｢繝峨′蜿悶ｌ縺溘ｉ蠕｡遉ｾ蜷阪・諡・ｽ楢・錐繧辿ubSpot縺ｫ險倬鹸縺吶ｋ</li>
                    <li key={2}>繝ｻ縲御ｻ頑律荳ｭ縺ｫ騾√ｊ縺ｾ縺吶阪→蜊ｳ陦悟虚繧堤ｴ・據縺吶ｋ縺薙→縺ｧ菫｡鬆ｼ諢溘ｒ蜃ｺ縺・/li>
                    <li key={3}>繝ｻ縲檎┌逅・↓豎ｺ繧√※繧ゅｉ繧上↑縺上※縺・＞縲坂・繝励Ξ繝・す繝｣繝ｼ繧貞､悶＠縺ｦ逶ｸ謇九・髦ｲ陦帛ｿ・ｒ荳九￡繧・/li>
                  </ul>
                </div>
              </div>

            </div>
          </div>

                    {/* 笏笏 譁ｭ繧頑枚蜿･蛻･蛻・ｊ霑斐＠・・T陬懷勧驥題ｨｴ豎ゑｼ・笏笏 */}
          <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
            <h2 className="text-base font-bold text-white mb-4">売 譁ｭ繧頑枚蜿･蛻･ 蛻・ｊ霑斐＠・・T陬懷勧驥題ｨｴ豎ゑｼ・/h2>
            <div className="space-y-3">
              {[
                { obj: '縲御ｺ育ｮ励′縺ｪ縺・阪後♀驥代′縺九°繧九・, res: '縲栗T陬懷勧驥代ｒ豢ｻ逕ｨ縺励※縺・◆縺縺上→蠑顔､ｾ縺檎筏隲九ｒ蜈ｨ縺ｦ莉｣陦後＠縺ｾ縺吶・縺ｧ縲゜IOSK蝙九′48荳・・縲懊√ち繝悶Ξ繝・ヨ蝙九′13荳・・縲懊〒縺泌ｰ主・縺ｧ縺阪∪縺吶よ怦鬘崎ｲｻ逕ｨ繧ゆｽｿ繧上↑縺・怦縺ｯ0蜀・↑縺ｮ縺ｧ縲∫ｹ∝ｿ呎悄縺縺代・縺泌茜逕ｨ繧ょ庄閭ｽ縺ｧ縺吶りｳ・侭縺縺代〒繧ゅ＃隕ｧ縺ｫ縺ｪ繧翫∪縺帙ｓ縺具ｼ溘・ },
                { obj: '縲御ｻ也､ｾ陬ｽ蜩√ｒ讀懆ｨ弱・菴ｿ逕ｨ荳ｭ縲・, res: '縲悟ｼ顔､ｾ縺ｯ繧ｷ繝ｪ繝ｳ繝繝ｼ骭蟇ｾ蠢懊・螳悟・繧ｪ繝ｼ繝繝ｼ繝｡繧､繝峨き繧ｹ繧ｿ繝槭う繧ｺ縺ｨ縺・≧轤ｹ縺ｧ蟾ｮ蛻･蛹悶〒縺阪※縺・∪縺吶ゅ∪縺櫑T陬懷勧驥代・逕ｳ隲倶ｻ｣陦後・蠑顔､ｾ縺ｮ蠑ｷ縺ｿ縺ｧ縺吶よｯ碑ｼ・､懆ｨ弱・雉・侭縺ｨ縺励※縺企√ｊ縺励※繧ゅｈ繧阪＠縺・〒縺励ｇ縺・°・溘・ },
                { obj: '縲御ｻ翫・譎よ悄縺梧が縺・阪梧擂蟷ｴ莉･髯阪〒縲・, res: '縲栗T陬懷勧驥代・逕ｳ隲区棧縺ｯ豈主ｹｴ譖ｴ譁ｰ縺輔ｌ縺ｾ縺吶・縺ｧ縲∽ｻ翫☆縺舌〒縺ｪ縺上※繧よュ蝣ｱ縺縺第戟縺｣縺ｦ縺翫＞縺ｦ縺・◆縺縺上→縲√ち繧､繝溘Φ繧ｰ縺梧擂縺滓凾縺ｫ縺吶＄蜍輔￠縺ｾ縺吶ゅΓ繝ｼ繝ｫ繧｢繝峨Ξ繧ｹ繧偵♀謨吶∴縺・◆縺縺代∪縺吶°・溘・ },
                { obj: '縲瑚｣懷勧驥代▲縺ｦ菴輔〒縺吶°・溘・, res: '縲栗T蟆主・陬懷勧驥代→縺・≧繧ゅ・縺ｧ縲∽ｸｭ蟆丈ｼ∵･ｭ讒倥′IT繧ｷ繧ｹ繝・Β繧貞ｰ主・縺吶ｋ髫帙↓蝗ｽ縺瑚ｲｻ逕ｨ縺ｮ譛螟ｧ2/3繧定｣懷勧縺励※縺上ｌ繧句宛蠎ｦ縺ｧ縺吶ょｼ顔､ｾ縺ｯ逕ｳ隲区焔邯壹″繧貞・縺ｦ莉｣陦後＠縺ｦ縺翫ｊ縺ｾ縺吶・縺ｧ縲∝ｾ｡遉ｾ縺ｯ譖ｸ鬘槭ｒ謠・∴縺ｦ縺・◆縺縺上□縺代〒OK縺ｧ縺吶ゅ・ },
                { obj: '縲檎┌莠ｺ縺ｫ縺ｯ縺ｧ縺阪↑縺・阪梧磁螳｢縺悟､ｧ蛻・・, res: '縲後檎怐莠ｺ蛹悶阪・縺疲署譯医〒縺吶ゅメ繧ｧ繝・け繧､繝ｳ謇狗ｶ壹″繧呈ｩ滓｢ｰ縺ｫ莉ｻ縺帙ｋ縺薙→縺ｧ縲√せ繧ｿ繝・ヵ縺瑚ｦｳ蜈画｡亥・繧・♀蜃ｺ霑弱∴縺ｪ縺ｩ譛ｬ譚･縺ｮ謗･螳｢縺ｫ髮・ｸｭ縺ｧ縺阪∪縺吶・T陬懷勧驥第ｴｻ逕ｨ縺ｧ螳溯ｳｪ雋ｻ逕ｨ繧ょ､ｧ蟷・↓謚代∴繧峨ｌ縺ｾ縺吶＠縲∬ｳ・侭縺縺代〒繧ゅ＞縺九′縺ｧ縺励ｇ縺・°・溘・ },
              ].map((item, i) => (
                <div key={i} className="bg-slate-700/50 rounded-xl p-4">
                  <p className="text-sm font-bold text-red-400 mb-2">笶・{item.obj}</p>
                  <div className="flex items-start gap-3">
                    <p className="text-base text-slate-200 leading-relaxed flex-1">笨・{item.res}</p>
                    <button onClick={() => copy(item.res, `ym_obj2_${i}`)} className={`text-xs px-3 py-1 rounded-lg font-medium flex-shrink-0 transition-colors ${copiedKey === `ym_obj2_${i}` ? 'bg-green-600 text-white' : 'bg-slate-600 text-slate-300 hover:bg-slate-500'}`}>
                      {copiedKey === `ym_obj2_${i}` ? '笨・ : '搭'}
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* 笏笏 AI蛻・ｊ霑斐＠繧ｵ繧ｸ繧ｧ繧ｹ繝・(Gemini API) 笏笏 */}
          <div className="bg-slate-900 rounded-2xl border border-purple-800/50 p-6">
            <div className="flex items-center justify-between mb-1">
              <h2 className="text-xl font-bold text-white">､・AI蛻・ｊ霑斐＠繧ｵ繧ｸ繧ｧ繧ｹ繝・/h2>
              <span className="text-xs bg-purple-900/60 border border-purple-700/50 text-purple-300 px-2 py-1 rounded-lg">Gemini API</span>
            </div>
            <p className="text-sm text-slate-400 mb-4">逶ｸ謇九′險縺｣縺溘％縺ｨ繧偵◎縺ｮ縺ｾ縺ｾ蜈･蜉・竊・AI縺後ョ繝舌う繧ｹ繧ｨ繝ｼ繧ｸ繧ｧ繝ｳ繧ｷ繝ｼ縺ｮ陬ｽ蜩∝・繧願ｿ斐＠繧定｡ｨ遉ｺ</p>
            <div className="flex gap-2 mb-4">
              <button onClick={() => setAiPattern('yoneyama')}
                className={`px-4 py-2 rounded-xl text-sm font-bold transition-all ${aiPattern === 'yoneyama' ? 'bg-yellow-600 text-white' : 'bg-slate-700 text-slate-300 border border-slate-600'}`}>
                腸 邀ｳ螻ｱ繝代ち繝ｼ繝ｳ・・T陬懷勧驥題ｨｴ豎ゑｼ・              </button>
              <button onClick={() => setAiPattern('hashimoto')}
                className={`px-4 py-2 rounded-xl text-sm font-bold transition-all ${aiPattern === 'hashimoto' ? 'bg-blue-600 text-white' : 'bg-slate-700 text-slate-300 border border-slate-600'}`}>
                町 讖区悽繝代ち繝ｼ繝ｳ・医ヲ繧｢繝ｪ繝ｳ繧ｰ蝙具ｼ・              </button>
            </div>
            <div className="flex gap-2 mb-4">
              <div className="relative flex-1">
                <span className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 text-lg">痔</span>
                <input type="text" value={aiInput} onChange={e => setAiInput(e.target.value)}
                  onKeyDown={e => e.key === 'Enter' && fetchAiSuggestions(aiInput, aiPattern)}
                  placeholder="萓具ｼ壹後ｂ縺・ｻ也､ｾ縺ｮ繧ｷ繧ｹ繝・Β蜈･繧後※縺ｾ縺吶阪御ｻ翫・蠢吶＠縺上※縲阪碁ｫ倥◎縺・□縺ｪ縲・
                  className="w-full bg-slate-800 border border-slate-600 rounded-xl pl-11 pr-4 py-4 text-base text-white placeholder-slate-500 focus:outline-none focus:border-purple-500 focus:ring-2 focus:ring-purple-500/30" />
                {aiInput && <button onClick={() => { setAiInput(''); setAiSuggestions([]); setAiSelectedIdx(null) }}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-white text-xl">ﾃ・/button>}
              </div>
              <button onClick={() => fetchAiSuggestions(aiInput, aiPattern)} disabled={!aiInput.trim() || aiLoading}
                className={`px-6 py-4 rounded-xl text-base font-bold transition-all whitespace-nowrap ${aiLoading ? 'bg-purple-900 text-purple-400 cursor-wait' : aiInput.trim() ? 'bg-purple-600 hover:bg-purple-500 text-white' : 'bg-slate-700 text-slate-500 cursor-not-allowed'}`}>
                {aiLoading ? '竢ｳ 逕滓・荳ｭ...' : '笨ｨ AI謠先｡・}
              </button>
            </div>
            {aiError && <div className="bg-red-950/50 border border-red-700/50 rounded-xl p-4 mb-4 text-sm text-red-300">笞・・{aiError}</div>}
            {aiLoading && <div className="text-center py-8 text-purple-400"><div className="text-2xl mb-2 animate-pulse">､・/div><p className="text-sm">Gemini AI縺悟・繧願ｿ斐＠繧堤函謌蝉ｸｭ...</p></div>}
            {aiSuggestions.length > 0 && (
              <div>
                <p className="text-sm text-purple-400 font-bold mb-3">庁 AI謗ｨ螂ｨ蛻・ｊ霑斐＠ ({aiSuggestions.length}莉ｶ)</p>
                <div className="flex flex-wrap gap-3 mb-4">
                  {aiSuggestions.map((s, i) => (
                    <button key={i} onClick={() => setAiSelectedIdx(aiSelectedIdx === i ? null : i)}
                      className={`px-5 py-3 rounded-xl text-base font-bold transition-all ${aiSelectedIdx === i ? 'bg-purple-600 text-white shadow-lg scale-105' : 'bg-purple-900/50 text-purple-200 hover:bg-purple-700 hover:text-white border border-purple-700/60'}`}>
                      {s.label}
                    </button>
                  ))}
                </div>
                {aiSelectedIdx !== null && aiSuggestions[aiSelectedIdx] && (
                  <div className="bg-purple-950/60 border-2 border-purple-700/70 rounded-2xl p-6">
                    <div className="flex items-center justify-between mb-3">
                      <div>
                        <p className="text-base text-purple-400 font-bold">町 {aiSuggestions[aiSelectedIdx].label}</p>
                        <p className="text-xs text-purple-300/70 mt-0.5">東 {aiSuggestions[aiSelectedIdx].point}</p>
                      </div>
                      <button onClick={() => copy(aiSuggestions[aiSelectedIdx!].talk, 'ai_suggest')}
                        className={`px-5 py-2 rounded-xl text-sm font-bold transition-colors ${copiedKey === 'ai_suggest' ? 'bg-purple-600 text-white' : 'bg-slate-700 hover:bg-slate-600 text-slate-200'}`}>
                        {copiedKey === 'ai_suggest' ? '笨・繧ｳ繝斐・貂医∩' : '搭 繧ｳ繝斐・'}
                      </button>
                    </div>
                    <p className="text-lg text-white leading-relaxed font-medium">{aiSuggestions[aiSelectedIdx].talk}</p>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* 笏笏 繝｡繝｢谺・笏笏 */}
          <div className="bg-slate-900 rounded-2xl border border-amber-800/50 p-6">
            {/* 繝倥ャ繝繝ｼ */}
            <div className="flex items-center justify-between mb-4">
              <div>
                <h2 className="text-xl font-bold text-white">統 譫ｶ髮ｻ繝｡繝｢</h2>
                <p className="text-sm text-slate-400 mt-0.5">騾夊ｩｱ荳ｭ縺ｮ繝｡繝｢繝ｻ豌励↓縺ｪ縺｣縺溽せ繧定ｨ倬鹸縲ゆｸ譎ゆｿ晏ｭ倥☆繧九→螻･豁ｴ縺ｫ谿九ｊ縺ｾ縺吶・/p>
              </div>
              <button
                onClick={() => setMemoOpen(o => !o)}
                className="text-slate-400 hover:text-white text-sm px-3 py-1.5 rounded-lg bg-slate-800 border border-slate-700 hover:border-slate-500 transition-colors"
              >
                {memoOpen ? '笆ｲ 髢峨§繧・ : '笆ｼ 髢九￥'}
              </button>
            </div>

            {memoOpen && (
              <div className="space-y-4">
                {/* 繝・く繧ｹ繝医お繝ｪ繧｢ */}
                <textarea
                  value={memoText}
                  onChange={e => {
                    setMemoText(e.target.value)
                    localStorage.setItem(MEMO_KEY, e.target.value)
                  }}
                  rows={6}
                  placeholder={`騾夊ｩｱ繝｡繝｢繧偵％縺薙↓蜈･蜉・..\n萓具ｼ噂n繝ｻ諡・ｽ難ｼ壼ｱｱ逕ｰ謾ｯ驟堺ｺｺ\n繝ｻ諛ｸ蠢ｵ・壹さ繧ｹ繝医√す繝ｪ繝ｳ繝繝ｼ骭\n繝ｻ谺｡蝗橸ｼ・/5 14:00 蜀肴楔髮ｻ`}
                  className="w-full bg-slate-800 border border-slate-600 rounded-xl px-4 py-3 text-base text-white placeholder-slate-500 focus:outline-none focus:border-amber-500 focus:ring-2 focus:ring-amber-500/30 resize-none leading-relaxed font-mono"
                />

                {/* 繝懊ち繝ｳ陦・*/}
                <div className="flex flex-wrap gap-3 items-center">
                  <button
                    onClick={saveMemo}
                    disabled={!memoText.trim()}
                    className={`px-6 py-3 rounded-xl text-base font-bold transition-all ${
                      memoSaved
                        ? 'bg-green-600 text-white'
                        : memoText.trim()
                          ? 'bg-amber-600 hover:bg-amber-500 text-white'
                          : 'bg-slate-700 text-slate-500 cursor-not-allowed'
                    }`}
                  >
                    {memoSaved ? '笨・菫晏ｭ俶ｸ医∩' : '沈 荳譎ゆｿ晏ｭ・}
                  </button>
                  <button
                    onClick={() => copy(memoText, 'memo')}
                    disabled={!memoText.trim()}
                    className={`px-6 py-3 rounded-xl text-base font-bold transition-all ${
                      copiedKey === 'memo'
                        ? 'bg-blue-600 text-white'
                        : memoText.trim()
                          ? 'bg-slate-700 hover:bg-slate-600 text-slate-200 border border-slate-600'
                          : 'bg-slate-800 text-slate-600 cursor-not-allowed border border-slate-700'
                    }`}
                  >
                    {copiedKey === 'memo' ? '笨・繧ｳ繝斐・貂医∩' : '搭 繧ｳ繝斐・'}
                  </button>
                  {memoText && (
                    <button
                      onClick={() => { setMemoText(''); localStorage.removeItem(MEMO_KEY) }}
                      className="px-4 py-3 rounded-xl text-sm text-slate-400 hover:text-red-400 hover:bg-red-950/30 border border-slate-700 transition-colors"
                    >
                      卵 繧ｯ繝ｪ繧｢
                    </button>
                  )}
                </div>

                {/* 菫晏ｭ伜ｱ･豁ｴ */}
                {savedMemos.length > 0 && (
                  <div className="border-t border-slate-700 pt-4">
                    <p className="text-sm font-bold text-slate-300 mb-3">武 菫晏ｭ伜ｱ･豁ｴ・域怙螟ｧ10莉ｶ・・/p>
                    <div className="space-y-2 max-h-64 overflow-y-auto pr-1">
                      {savedMemos.map((m, i) => (
                        <div key={i} className="bg-slate-800 rounded-xl border border-slate-700 px-4 py-3">
                          <div className="flex items-center justify-between mb-1.5">
                            <span className="text-xs text-amber-400 font-bold">{m.ts}</span>
                            <div className="flex gap-2">
                              <button
                                onClick={() => { setMemoText(m.text); localStorage.setItem(MEMO_KEY, m.text) }}
                                className="text-xs text-blue-400 hover:text-blue-300 px-2 py-0.5 rounded bg-blue-950/40 border border-blue-800/40"
                              >
                                蠕ｩ蜈・                              </button>
                              <button
                                onClick={() => copy(m.text, `saved_${i}`)}
                                className="text-xs text-slate-400 hover:text-white px-2 py-0.5 rounded bg-slate-700/60 border border-slate-600"
                              >
                                {copiedKey === `saved_${i}` ? '笨・ : '搭'}
                              </button>
                              <button
                                onClick={() => deleteSavedMemo(i)}
                                className="text-xs text-red-400 hover:text-red-300 px-2 py-0.5 rounded bg-red-950/40 border border-red-800/40"
                              >
                                蜑企勁
                              </button>
                            </div>
                          </div>
                          <p className="text-sm text-slate-300 whitespace-pre-line leading-relaxed line-clamp-3">{m.text}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>


        </div>
      )}

      {/* 笏笏笏 TAB: 邀ｳ螻ｱ繝代ち繝ｼ繝ｳ 笏笏笏 */}
      {activeTab === 'yoneyama' && (
        <div className="space-y-6">
          <div className="bg-gradient-to-r from-yellow-900/40 to-orange-900/40 border border-yellow-700/50 rounded-2xl p-6">
            <div className="flex items-center gap-3 mb-3">
              <span className="text-3xl">腸</span>
              <div>
                <h2 className="text-xl font-bold text-white">邀ｳ螻ｱ繝代ち繝ｼ繝ｳ 窶・IT陬懷勧驥大・髱｢險ｴ豎ょ梛</h2>
                <p className="text-sm text-yellow-300/80 mt-0.5">IT陬懷勧驥代ｒ蜑埼擇縺ｫ蜃ｺ縺励・025蟷ｴ繝・Ξ繧｢繝昴ヨ繝ｬ繝ｳ繝峨ｒ蜿肴丐縺励◆繧ｹ繧ｯ繝ｪ繝励ヨ</p>
              </div>
            </div>
          </div>

          <div className="bg-slate-900 rounded-2xl border border-yellow-800/50 p-6">
            <div className="flex items-center justify-between mb-1">
              <h2 className="text-xl font-bold text-white">､・AI蛻・ｊ霑斐＠・育ｱｳ螻ｱ繝代ち繝ｼ繝ｳ蟆ら畑・・/h2>
              <span className="text-xs bg-yellow-900/60 border border-yellow-700/50 text-yellow-300 px-2 py-1 rounded-lg">Gemini API</span>
            </div>
            <p className="text-sm text-slate-400 mb-4">逶ｸ謇九・逋ｺ險繧貞・蜉・竊・IT陬懷勧驥題ｨｴ豎ゅｒ蜷ｫ繧蛻・ｊ霑斐＠繧但I縺檎函謌・/p>
            <div className="flex gap-2 mb-4">
              <div className="relative flex-1">
                <span className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 text-lg">痔</span>
                <input type="text" value={yoneyamaInput} onChange={e => setYoneyamaInput(e.target.value)}
                  onKeyDown={e => e.key === 'Enter' && fetchYoneyamaSuggestions(yoneyamaInput)}
                  placeholder="萓具ｼ壹御ｺ育ｮ励′縺ｪ縺・阪御ｻ也､ｾ縺ｧ讀懆ｨ惹ｸｭ縲阪御ｻ翫・譎よ悄縺梧が縺・・
                  className="w-full bg-slate-800 border border-slate-600 rounded-xl pl-11 pr-4 py-4 text-base text-white placeholder-slate-500 focus:outline-none focus:border-yellow-500 focus:ring-2 focus:ring-yellow-500/30" />
                {yoneyamaInput && <button onClick={() => { setYoneyamaInput(''); setYoneyamaSuggestions([]); setYoneyamaSelectedIdx(null) }}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-white text-xl">ﾃ・/button>}
              </div>
              <button onClick={() => fetchYoneyamaSuggestions(yoneyamaInput)} disabled={!yoneyamaInput.trim() || yoneyamaLoading}
                className={`px-6 py-4 rounded-xl text-base font-bold transition-all whitespace-nowrap ${yoneyamaLoading ? 'bg-yellow-900 text-yellow-400 cursor-wait' : yoneyamaInput.trim() ? 'bg-yellow-600 hover:bg-yellow-500 text-white' : 'bg-slate-700 text-slate-500 cursor-not-allowed'}`}>
                {yoneyamaLoading ? '竢ｳ 逕滓・荳ｭ...' : '笨ｨ AI謠先｡・}
              </button>
            </div>
            {yoneyamaError && <div className="bg-red-950/50 border border-red-700/50 rounded-xl p-4 mb-4 text-sm text-red-300">笞・・{yoneyamaError}</div>}
            {yoneyamaLoading && <div className="text-center py-8 text-yellow-400"><div className="text-2xl mb-2 animate-pulse">､・/div><p className="text-sm">Gemini AI縺檎ｱｳ螻ｱ繝代ち繝ｼ繝ｳ縺ｧ逕滓・荳ｭ...</p></div>}
            {yoneyamaSuggestions.length > 0 && (
              <div>
                <p className="text-sm text-yellow-400 font-bold mb-3">庁 AI謗ｨ螂ｨ蛻・ｊ霑斐＠ ({yoneyamaSuggestions.length}莉ｶ)</p>
                <div className="flex flex-wrap gap-3 mb-4">
                  {yoneyamaSuggestions.map((s, i) => (
                    <button key={i} onClick={() => setYoneyamaSelectedIdx(yoneyamaSelectedIdx === i ? null : i)}
                      className={`px-5 py-3 rounded-xl text-base font-bold transition-all ${yoneyamaSelectedIdx === i ? 'bg-yellow-600 text-white shadow-lg scale-105' : 'bg-yellow-900/50 text-yellow-200 hover:bg-yellow-700 hover:text-white border border-yellow-700/60'}`}>
                      {s.label}
                    </button>
                  ))}
                </div>
                {yoneyamaSelectedIdx !== null && yoneyamaSuggestions[yoneyamaSelectedIdx] && (
                  <div className="bg-yellow-950/60 border-2 border-yellow-700/70 rounded-2xl p-6">
                    <div className="flex items-center justify-between mb-3">
                      <div>
                        <p className="text-base text-yellow-400 font-bold">町 {yoneyamaSuggestions[yoneyamaSelectedIdx].label}</p>
                        <p className="text-xs text-yellow-300/70 mt-0.5">東 {yoneyamaSuggestions[yoneyamaSelectedIdx].point}</p>
                      </div>
                      <button onClick={() => copy(yoneyamaSuggestions[yoneyamaSelectedIdx!].talk, 'yoneyama_ai')}
                        className={`px-5 py-2 rounded-xl text-sm font-bold transition-colors ${copiedKey === 'yoneyama_ai' ? 'bg-yellow-600 text-white' : 'bg-slate-700 hover:bg-slate-600 text-slate-200'}`}>
                        {copiedKey === 'yoneyama_ai' ? '笨・繧ｳ繝斐・貂医∩' : '搭 繧ｳ繝斐・'}
                      </button>
                    </div>
                    <p className="text-lg text-white leading-relaxed font-medium">{yoneyamaSuggestions[yoneyamaSelectedIdx].talk}</p>
                  </div>
                )}
              </div>
            )}
          </div>

          <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
            <h2 className="text-xl font-bold text-white mb-4">到 邀ｳ螻ｱ繝代ち繝ｼ繝ｳ 窶・繝医・繧ｯ繧ｹ繧ｯ繝ｪ繝励ヨ</h2>
            <div className="space-y-3">
              {[
                { label: '竭 繧ｪ繝ｼ繝励ル繝ｳ繧ｰ・亥女莉倡ｪ∫ｴ・・, color: 'blue', text: '縲後♀蠢吶＠縺・→縺薙ｍ諱舌ｌ蜈･繧翫∪縺吶ゅョ繝舌う繧ｹ繧ｨ繝ｼ繧ｸ繧ｧ繝ｳ繧ｷ繝ｼ縺ｮ邀ｳ螻ｱ縺ｧ縺斐＊縺・∪縺吶よ悽譌･縺ｯ縲√・繝・Ν繝ｻ譌・､ｨ讒伜髄縺代・IT陬懷勧驥第ｴｻ逕ｨ縺ｧ縺泌ｰ主・縺ｧ縺阪ｋ閾ｪ蜍輔メ繧ｧ繝・け繧､繝ｳ讖溘・縺疲｡亥・縺ｧ縺秘｣邨｡縺励∪縺励◆縲ゅ＃諡・ｽ楢・ｧ倥°縺疲髪驟堺ｺｺ讒倥・縺・ｉ縺｣縺励ｃ縺・∪縺吶〒縺励ｇ縺・°・溘・ },
                { label: '竭｡ IT陬懷勧驥代ｒ蜑埼擇縺ｫ蜃ｺ縺・, color: 'yellow', text: '縲悟ｼ顔､ｾ縺ｧ縺ｯ莉翫！T陬懷勧驥代・逕ｳ隲九ｒ蜈ｨ縺ｦ蠑顔､ｾ縺御ｻ｣陦後☆繧句ｽ｢縺ｧ縲∬・蜍輔メ繧ｧ繝・け繧､繝ｳ讖溘ｒ縺頑焔鬆・↑萓｡譬ｼ縺ｧ縺泌ｰ主・縺・◆縺縺代※縺・∪縺吶・IOSK蝙九′螳溯ｳｪ48荳・・縲懊√ち繝悶Ξ繝・ヨ蝙九′13荳・・縲懊→縺泌･ｽ隧輔＞縺溘□縺・※縺翫ｊ縺ｾ縺励※縲ょ｣ｲ繧願ｾｼ縺ｿ縺ｧ縺ｯ縺ｪ縺上∬｣懷勧驥第ｴｻ逕ｨ縺ｮ諠・ｱ繧偵♀莨昴∴縺励◆縺上※縺秘｣邨｡縺励∪縺励◆縲ゅ・ },
                { label: '竭｢ 繝偵い繝ｪ繝ｳ繧ｰ', color: 'purple', text: '縲梧怙霑代∵･ｭ逡悟・菴薙〒繧､繝ｳ繝舌え繝ｳ繝牙ｯｾ蠢懊ｄ莠ｺ謇倶ｸ崎ｶｳ縺ｮ縺雁｣ｰ繧偵ｈ縺上♀閨槭″縺吶ｋ縺ｮ縺ｧ縺吶′縲∝ｾ｡遉ｾ縺ｧ縺ｯ迴ｾ蝨ｨ縲∽ｽ輔°驕狗畑荳翫・隱ｲ鬘後・縺頑─縺倥〒縺吶°・溘・ },
                { label: '竭｣ YES 竊・謠先｡・, color: 'green', text: '縲後◎縺・〒縺吶ｈ縺ｭ縲ゅ◎縺ｮ隱ｲ鬘後ｒIT陬懷勧驥代ｒ豢ｻ逕ｨ縺励※隗｣豎ｺ縺輔ｌ縺滉ｺ倶ｾ九′謇句・縺ｫ縺ゅｊ縺ｾ縺吶りｳ・侭縺縺代〒繧ゅΓ繝ｼ繝ｫ縺ｧ縺企√ｊ縺励※繧ゅｈ繧阪＠縺・〒縺励ｇ縺・°・溘・ },
                { label: '竭､ NO 竊・諠・ｱ縺縺第署譯・, color: 'slate', text: '縲梧価遏･縺励∪縺励◆縲・T陬懷勧驥代・豈主ｹｴ逕ｳ隲区棧縺後≠繧翫∪縺吶・縺ｧ縲√ち繧､繝溘Φ繧ｰ縺梧擂縺滓凾縺ｮ縺溘ａ縺縺代〒繧りｳ・侭繧偵♀謇句・縺ｫ鄂ｮ縺・※縺・◆縺縺代ｌ縺ｰ縲ゅΓ繝ｼ繝ｫ繧｢繝峨Ξ繧ｹ繧偵♀謨吶∴縺・◆縺縺代∪縺吶°・溘・ },
              ].map((item, i) => (
                <div key={i} className={`rounded-xl p-4 ${item.color === 'blue' ? 'bg-blue-950/40 border border-blue-800/40' : item.color === 'yellow' ? 'bg-yellow-950/40 border border-yellow-800/40' : item.color === 'purple' ? 'bg-purple-950/40 border border-purple-800/40' : item.color === 'green' ? 'bg-green-950/40 border border-green-800/40' : 'bg-slate-700/50 border border-slate-600/40'}`}>
                  <div className="flex items-center justify-between mb-2">
                    <p className={`text-xs font-bold ${item.color === 'blue' ? 'text-blue-400' : item.color === 'yellow' ? 'text-yellow-400' : item.color === 'purple' ? 'text-purple-400' : item.color === 'green' ? 'text-green-400' : 'text-slate-400'}`}>{item.label}</p>
                    <button onClick={() => copy(item.text, `ym_${i}`)} className={`text-xs px-3 py-1 rounded-lg font-medium transition-colors ${copiedKey === `ym_${i}` ? 'bg-green-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}>
                      {copiedKey === `ym_${i}` ? '笨・ : '搭'}
                    </button>
                  </div>
                  <p className="text-sm text-slate-200 leading-relaxed">{item.text}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-slate-800 rounded-2xl border border-yellow-700/40 p-6">
            <h2 className="text-base font-bold text-white mb-4">売 譁ｭ繧頑枚蜿･蛻･ 蛻・ｊ霑斐＠・・T陬懷勧驥題ｨｴ豎ゑｼ・/h2>
            <div className="space-y-3">
              {[
                { obj: '縲御ｺ育ｮ励′縺ｪ縺・阪後♀驥代′縺九°繧九・, res: '縲後◎縺・〒縺吶ｈ縺ｭ縲ょｮ溘・IT陬懷勧驥代ｒ豢ｻ逕ｨ縺励※縺・◆縺縺上→縲∝ｼ顔､ｾ縺檎筏隲九ｒ蜈ｨ縺ｦ莉｣陦後＠縺ｾ縺吶・縺ｧ縲゜IOSK蝙九′48荳・・縲懊√ち繝悶Ξ繝・ヨ蝙九′13荳・・縲懊〒縺泌ｰ主・縺ｧ縺阪∪縺吶よ怦鬘崎ｲｻ逕ｨ繧ゆｽｿ繧上↑縺・怦縺ｯ0蜀・↑縺ｮ縺ｧ縲∫ｹ∝ｿ呎悄縺縺代・縺泌茜逕ｨ繧ょ庄閭ｽ縺ｧ縺吶りｳ・侭縺縺代〒繧ゅ＃隕ｧ縺ｫ縺ｪ繧翫∪縺帙ｓ縺具ｼ溘・ },
                { obj: '縲御ｻ也､ｾ陬ｽ蜩√ｒ讀懆ｨ弱・菴ｿ逕ｨ荳ｭ縲・, res: '縲悟ｼ顔､ｾ縺ｯ繧ｷ繝ｪ繝ｳ繝繝ｼ骭蟇ｾ蠢懊・螳悟・繧ｪ繝ｼ繝繝ｼ繝｡繧､繝峨き繧ｹ繧ｿ繝槭う繧ｺ縺ｨ縺・≧轤ｹ縺ｧ蟾ｮ蛻･蛹悶〒縺阪※縺・∪縺吶ゅ∪縺櫑T陬懷勧驥代・逕ｳ隲倶ｻ｣陦後・蠑顔､ｾ縺ｮ蠑ｷ縺ｿ縺ｧ縺吶よｯ碑ｼ・､懆ｨ弱・雉・侭縺ｨ縺励※縺企√ｊ縺励※繧ゅｈ繧阪＠縺・〒縺励ｇ縺・°・溘・ },
                { obj: '縲御ｻ翫・譎よ悄縺梧が縺・阪梧擂蟷ｴ莉･髯阪〒縲・, res: '縲栗T陬懷勧驥代・逕ｳ隲区棧縺ｯ豈主ｹｴ譖ｴ譁ｰ縺輔ｌ縺ｾ縺吶・縺ｧ縲∽ｻ翫☆縺舌〒縺ｪ縺上※繧よュ蝣ｱ縺縺第戟縺｣縺ｦ縺翫＞縺ｦ縺・◆縺縺上→縲√ち繧､繝溘Φ繧ｰ縺梧擂縺滓凾縺ｫ縺吶＄蜍輔￠縺ｾ縺吶ゆｻ頑律荳ｭ縺ｫ雉・侭繧偵Γ繝ｼ繝ｫ縺ｧ縺企√ｊ縺吶ｋ縺縺代〒縺吶・縺ｧ縲√Γ繝ｼ繝ｫ繧｢繝峨Ξ繧ｹ繧偵♀謨吶∴縺・◆縺縺代∪縺吶°・溘・ },
                { obj: '縲瑚｣懷勧驥代▲縺ｦ菴輔〒縺吶°・溘・, res: '縲栗T蟆主・陬懷勧驥代→縺・≧繧ゅ・縺ｧ縲∽ｸｭ蟆丈ｼ∵･ｭ讒倥′IT繧ｷ繧ｹ繝・Β繧貞ｰ主・縺吶ｋ髫帙↓蝗ｽ縺瑚ｲｻ逕ｨ縺ｮ譛螟ｧ2/3繧定｣懷勧縺励※縺上ｌ繧句宛蠎ｦ縺ｧ縺吶ょｼ顔､ｾ縺ｯ逕ｳ隲区焔邯壹″繧貞・縺ｦ莉｣陦後＠縺ｦ縺翫ｊ縺ｾ縺吶・縺ｧ縲∝ｾ｡遉ｾ縺ｯ譖ｸ鬘槭ｒ謠・∴縺ｦ縺・◆縺縺上□縺代〒OK縺ｧ縺吶ゅ・ },
              ].map((item, i) => (
                <div key={i} className="bg-slate-700/50 rounded-xl p-4">
                  <p className="text-sm font-bold text-red-400 mb-2">笶・{item.obj}</p>
                  <div className="flex items-start gap-3">
                    <p className="text-base text-slate-200 leading-relaxed flex-1">笨・{item.res}</p>
                    <button onClick={() => copy(item.res, `ym_obj_${i}`)} className={`text-xs px-3 py-1 rounded-lg font-medium flex-shrink-0 transition-colors ${copiedKey === `ym_obj_${i}` ? 'bg-green-600 text-white' : 'bg-slate-600 text-slate-300 hover:bg-slate-500'}`}>
                      {copiedKey === `ym_obj_${i}` ? '笨・ : '搭'}
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* 笏笏笏 TAB: 繧ｹ繝・・繧ｿ繧ｹ荳隕ｧ 笏笏笏 */}
      {activeTab === 'status' && (
        <div className="space-y-6">
          <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
            <h2 className="text-base font-bold text-white mb-4">笨・菴ｿ逕ｨ縺吶ｋ繧ｹ繝・・繧ｿ繧ｹ・亥叙蠑輔せ繝・・繧ｸ・・/h2>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-slate-700">
                    <th className="text-left text-slate-400 font-medium py-2 pr-4">繧ｹ繝・・繧ｿ繧ｹ</th>
                    <th className="text-left text-slate-400 font-medium py-2">逕ｨ騾・/th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-700/50">
                  {[
                    { status: '讌ｽ螟ｩ繝医Λ繝吶Ν・域悴譫ｶ髮ｻ・・, desc: '繧ｿ繝ｼ繧ｲ繝・ヨ繝ｪ繧ｹ繝・, badge: 'blue' },
                    { status: '讌ｽ螟ｩ繝医Λ繝吶Ν・井ｸ榊惠・・, desc: '諡・ｽ楢・ｸ榊惠譎ゑｼ郁ｳ・侭騾∽ｻ伜ｾ後・荳榊惠縺ｯ遘ｻ蜍穂ｸ崎ｦ・ｼ・, badge: 'yellow' },
                    { status: '讌ｽ螟ｩ繝医Λ繝吶Ν・域妙繧奇ｼ・, desc: '譁ｭ繧峨ｌ縺溷ｴ蜷・, badge: 'red' },
                    { status: '讌ｽ螟ｩ繝医Λ繝吶Ν・域悽遉ｾ縺ｸ・・, desc: '譛ｬ遉ｾ縺梧ｱｺ貂医・蝣ｴ蜷・, badge: 'purple' },
                    { status: '讌ｽ螟ｩ繝医Λ繝吶Ν・・蝗樒岼・・, desc: '1蝗樒岼縺ｮ繧｢繝励Ο繝ｼ繝・, badge: 'slate' },
                    { status: '雉・侭騾∽ｻ・, desc: '譫ｶ髮ｻ蠕後↓雉・侭騾∽ｻ倥↓閾ｳ縺｣縺溷ｴ蜷・, badge: 'green' },
                    { status: '譫ｶ髮ｻ繧ｯ繝ｬ繝ｼ繝', desc: '縲後°縺代※縺上ｋ縺ｪ縲阪↑縺ｩ險繧上ｌ縺溷ｴ蜷・, badge: 'red' },
                    { status: '譫ｶ髮ｻ繝ｪ繧ｹ繝茨ｼ井ｻ也､ｾ陬ｽ蜩∽ｽｿ逕ｨ・・, desc: '縺吶〒縺ｫ莉也､ｾ陬ｽ蜩√ｒ蟆主・貂医∩縺ｮ蝣ｴ蜷・, badge: 'slate' },
                    { status: '騾｣邨｡荳榊庄繝ｻIVR', desc: '髢画･ｭ繧・崕隧ｱ逡ｪ蜿ｷ縺御ｽｿ繧上ｌ縺ｦ縺・↑縺・ｴ蜷・, badge: 'slate' },
                    { status: '繧ｻ繝溘リ繝ｼ莠亥ｮ・, desc: '繧｢繝昴う繝ｳ繝育佐蠕励懷ｽ捺律縺ｾ縺ｧ', badge: 'green' },
                    { status: '繧ｻ繝溘リ繝ｼ蜿ょ刈', desc: '螳滄圀縺ｫ蜿ょ刈縺励◆蝣ｴ蜷・, badge: 'green' },
                    { status: '繧ｻ繝溘リ繝ｼ繧ｭ繝｣繝ｳ繧ｻ繝ｫ', desc: '繧ｭ繝｣繝ｳ繧ｻ繝ｫ縺檎匱逕溘＠縺溷ｴ蜷・, badge: 'red' },
                  ].map((row, i) => (
                    <tr key={i}>
                      <td className="py-3 pr-4">
                        <span className={`text-xs font-medium px-2 py-1 rounded-lg ${
                          row.badge === 'blue' ? 'bg-blue-900/60 text-blue-300' :
                          row.badge === 'green' ? 'bg-green-900/60 text-green-300' :
                          row.badge === 'yellow' ? 'bg-yellow-900/60 text-yellow-300' :
                          row.badge === 'red' ? 'bg-red-900/60 text-red-300' :
                          row.badge === 'purple' ? 'bg-purple-900/60 text-purple-300' :
                          'bg-slate-700 text-slate-300'
                        }`}>{row.status}</span>
                      </td>
                      <td className="text-slate-300 py-3 text-sm">{row.desc}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
            <h2 className="text-base font-bold text-white mb-4">白 繝ｪ繝ｼ繝峨せ繝・・繧ｿ繧ｹ縺ｮ遞ｮ蛻･</h2>
            <div className="space-y-3">
              {[
                { label: '雉・侭騾∽ｻ・騾ｱ髢謎ｻ･蜀・, desc: '繧ｿ繧ｹ繧ｯ繧定ｨｭ螳壹ゆｻｶ蜷阪瑚ｳ・侭騾∽ｻ・縲・縲・阪よ悄髯舌・3騾ｱ髢灘ｾ後りｳ・侭騾∽ｻ俶焚縺ｮ險育ｮ励↓菴ｿ縺・・, color: 'blue' },
                { label: '雉・侭騾∽ｻ倥う繝ｳ繧ｻ繝ｳ繝・ぅ繝悶↑縺・, desc: '繧｢繝昴う繝ｳ繝医ｒ蜿悶ｊ縺ｫ陦後￥縺溘ａ縺ｫ繧ｿ繧ｹ繧ｯ繧定ｨｭ螳壹よ球蠖楢・・蜿嶺ｻ倥・蜿梧婿縺ｮ蜷榊燕繧定◇縺代↑縺九▲縺溷ｴ蜷医・繧､繝ｳ繧ｻ繝ｳ縺ｪ縺励・, color: 'yellow' },
                { label: '雉・侭騾∽ｻ假ｼ九そ繝溘リ繝ｼ蜿ょ刈', desc: '繧ｻ繝溘リ繝ｼ蜿ょ刈繧､繝ｳ繧ｻ繝ｳ繝・ぅ繝也佐蠕玲凾縲ょ叙蠑輔せ繝・・繧ｸ縺ｯ縲舌そ繝溘リ繝ｼ莠亥ｮ壹代∈縲・, color: 'green' },
              ].map((item, i) => (
                <div key={i} className={`rounded-xl p-4 ${
                  item.color === 'blue' ? 'bg-blue-950/40 border border-blue-800/40' :
                  item.color === 'yellow' ? 'bg-yellow-950/40 border border-yellow-800/40' :
                  'bg-green-950/40 border border-green-800/40'
                }`}>
                  <p className={`text-xs font-bold mb-1 ${
                    item.color === 'blue' ? 'text-blue-400' :
                    item.color === 'yellow' ? 'text-yellow-400' : 'text-green-400'
                  }`}>{item.label}</p>
                  <p className="text-sm text-slate-300">{item.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* 笏笏笏 TAB: 蝠・刀遏･隴・笏笏笏 */}
      {activeTab === 'knowledge' && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
              <h2 className="text-base font-bold text-white mb-4">妾 陬ｽ蜩√Λ繧､繝ｳ繝翫ャ繝・/h2>
              <div className="space-y-3">
                {[
                  { name: '閾ｪ蜍輔メ繧ｧ繝・け繧､繝ｳ讖滂ｼ・IOSK蝙具ｼ・, desc: '縺吶∋縺ｦ縺ｮ貂・ｮ玲ｩ溯・縺ゅｊ縲ら筏霎ｼ縺九ｉ3繝ｶ譛医〒謇矩・蜿ｯ閭ｽ縲・, badge: 'blue' },
                  { name: '閾ｪ蜍輔メ繧ｧ繝・け繧､繝ｳ讖滂ｼ医ち繝悶Ξ繝・ヨ蝙具ｼ・, desc: '蟆剰ｦ乗ｨ｡譁ｽ險ｭ繝ｻ豌第ｳ雁髄縺代ら筏霎ｼ縺九ｉ1繝ｶ譛医〒謇矩・蜿ｯ閭ｽ縲・, badge: 'green' },
                  { name: '繧ｯ繝ｩ繧ｦ繝峨せ繝槭・繝医Ο繝・け', desc: '證苓ｨｼ逡ｪ蜿ｷ縺ｧ髢矩権縲ゅメ繧ｧ繝・け繧､繝ｳ讖溘→騾｣蜍輔＠縺ｦ繝ｬ繧ｷ繝ｼ繝医↓證苓ｨｼ逡ｪ蜿ｷ繧貞魂蟄励・, badge: 'purple' },
                  { name: '繝ｫ繝ｼ繝繧ｿ繝悶Ξ繝・ヨ', desc: '蜀・ｷ夐崕隧ｱ讖溯・縲ゅせ繧ｿ繝・ヵ縺ｮ蜷榊燕陦ｨ遉ｺ繝ｻ螟夊ｨ隱槫ｯｾ蠢懊よ怦鬘・螳､100蜀・・, badge: 'yellow' },
                ].map((p, i) => (
                  <div key={i} className="bg-slate-700/50 rounded-xl p-4">
                    <p className={`text-xs font-bold mb-1 ${
                      p.badge === 'blue' ? 'text-blue-400' : p.badge === 'green' ? 'text-green-400' :
                      p.badge === 'purple' ? 'text-purple-400' : 'text-yellow-400'
                    }`}>{p.name}</p>
                    <p className="text-sm text-slate-300">{p.desc}</p>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
              <h2 className="text-base font-bold text-white mb-4">腸 萓｡譬ｼ繝ｻ雋ｻ逕ｨ諢・/h2>
              <div className="space-y-3">
                <div className="bg-slate-700/50 rounded-xl p-4">
                  <p className="text-sm font-bold text-blue-400 mb-2">蛻晄悄雋ｻ逕ｨ・・T陬懷勧驥第ｴｻ逕ｨ譎ゑｼ・/p>
                  <ul className="text-sm text-slate-300 space-y-1">
                    <li>繝ｻKIOSK蝙具ｼ・span className="text-white font-bold">48荳・・縲・/span></li>
                    <li>繝ｻ繧ｿ繝悶Ξ繝・ヨ蝙具ｼ・span className="text-white font-bold">13荳・・縲・/span></li>
                    <li>繝ｻ荳霆貞ｮｶ・医す繝ｳ繧ｰ繝ｫ繝励Λ繝ｳ・会ｼ・span className="text-white font-bold">49,800蜀・・/span></li>
                    <li className="text-xs text-slate-500">窶ｻ陬懷勧驥醍筏隲九・蠑顔､ｾ縺瑚｡後≧</li>
                  </ul>
                </div>
                <div className="bg-slate-700/50 rounded-xl p-4">
                  <p className="text-sm font-bold text-green-400 mb-2">譛磯｡崎ｲｻ逕ｨ</p>
                  <ul className="text-sm text-slate-300 space-y-1">
                    <li>繝ｻKIOSK蝙具ｼ・9,600蜀・ｼ矩Κ螻区焚ﾃ・00蜀・/li>
                    <li>繝ｻ繧ｿ繝悶Ξ繝・ヨ蝙具ｼ・00蜀・鈴Κ螻区焚</li>
                    <li>繝ｻ菴ｿ逕ｨ縺励↑縺・怦縺ｯ<span className="text-green-300 font-medium">譛磯｡・蜀・/span></li>
                    <li>繝ｻ蝨滓律逾昴・縺ｿ菴ｿ逕ｨ縺ｮ譌･蜑ｲ繧願ｨ育ｮ励ｂ蜿ｯ閭ｽ</li>
                  </ul>
                </div>
              </div>
            </div>

            <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
              <h2 className="text-base font-bold text-white mb-4">笶・繧医￥縺ゅｋ雉ｪ蝠上→蝗樒ｭ・/h2>
              <div className="space-y-3">
                {[
                  { q: 'PMS縺ｨ騾｣謳ｺ縺ｧ縺阪ｋ縺ｮ・・, a: '蠑顔､ｾ縺ｯPMS縺ｨ縺ｮ騾｣謳ｺ髢狗匱縺ｫ霑大ｹｴ蜉帙ｒ蜈･繧後※縺・∪縺吶ょｮ溽ｸｾ・壹せ繝・う繧ｷ繝ｼ縲√せ繧､繝ｼ繝医ヶ繝・け縲√・繝・ヤ24縲ゅ♀螳｢讒倥・隕∵悍縺ｫ繧医ｊ縺九↑繧翫・鬆ｻ蠎ｦ縺ｧ髢狗匱騾｣謳ｺ縺碁ｲ繧薙〒縺・∪縺吶・縺ｧ縲∝ｾ｡遉ｾ縺ｮPMS繧ゆｻ雁ｾ碁｣謳ｺ髢狗匱繧帝ｲ繧√∪縺吶・ },
                  { q: '繧ｫ繝ｼ繝峨く繝ｼ縺ｫ螟峨∴縺ｪ縺・→縺・￠縺ｪ縺・ｼ・, a: '蠑顔､ｾ縺ｮ螢ｲ繧翫・繧ｷ繝ｪ繝ｳ繝繝ｼ骭・育黄逅・く繝ｼ・峨↓蟇ｾ蠢懷庄閭ｽ縺ｪ縺薙→縲ょ挨螢ｲ繧翫・繧ｭ繝ｼ繝懊ャ繧ｯ繧ｹ縺ｧ貂・ｮ怜ｾ後↓繧ｭ繝ｼ縺瑚・蜍暮幕謾ｾ縺輔ｌ繧九ゅく繝ｼ繝懊ャ繧ｯ繧ｹ縺ｪ縺励〒繧ゅΞ繧ｷ繝ｼ繝医ｒ繝輔Ο繝ｳ繝医〒骰ｵ縺ｨ莠､謠帙☆繧句ｯｾ髱｢謗･螳｢繧よｮ九○繧九・ },
                  { q: '縲檎┌莠ｺ縲阪↓縺ｧ縺阪∪縺吶°・・, a: '笞・上檎┌莠ｺ縲阪→縺・≧繝ｯ繝ｼ繝峨・NG縲ゅ檎怐莠ｺ蛹悶・讌ｭ蜍吝柑邇・喧縲阪→陦ｨ迴ｾ縺吶ｋ縲ゅヵ繝ｭ繝ｳ繝医せ繧ｿ繝・ヵ縺ｮ讌ｭ蜍吶ｒ蜑頑ｸ帙＠縲∵磁螳｢繧ｵ繝ｼ繝薙せ縺ｫ髮・ｸｭ縺ｧ縺阪ｋ迺ｰ蠅・ｒ菴懊ｋ縺薙→繧単R縺吶ｋ縲・ },
                  { q: '繧､繝ｳ繝舌え繝ｳ繝牙ｯｾ蠢懊・・・, a: '螟夊ｨ隱槫ｯｾ蠢懶ｼ・2縲・3縺句嵜隱橸ｼ峨√ヱ繧ｹ繝昴・繝医せ繧ｭ繝｣繝ｳ繝ｻ譛ｬ莠ｺ遒ｺ隱肴ｩ溯・縺ゅｊ縲ゅう繝ｳ繝舌え繝ｳ繝牙ｯｾ遲悶↓髱槫ｸｸ縺ｫ譛牙柑縲・ },
                ].map((item, i) => (
                  <div key={i} className="bg-slate-700/50 rounded-xl p-4">
                    <p className="text-sm font-bold text-yellow-400 mb-2">Q: {item.q}</p>
                    <p className="text-base text-slate-200 leading-relaxed">A: {item.a}</p>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
              <h2 className="text-base font-bold text-white mb-4">謄 讌ｭ蜍呎欠蟆弱・驥崎ｦ√・繧､繝ｳ繝・/h2>
              <div className="space-y-2 max-h-96 overflow-y-auto pr-1">
                {[
                  '雉・侭騾∽ｻ伜ｾ・騾ｱ髢謎ｻ･蜀・・蜀肴楔髮ｻ繧貞ｾｹ蠎輔・00蜀・・繧､繝ｳ繧ｻ繝ｳ繧医ｊ5,000蜀・・繧｢繝昴う繝ｳ繝医ｒ迢吶≧蝓ｷ逹蠢・ｒ謖√▽縲・,
                  '縲悟ｰ・擂逧・↓縺碑・蜻ｳ縺ゅｊ縺ｾ縺吶°・溘阪〒謠先｡医☆繧九ゅ御ｻ雁ｰ主・縺励※縺ｾ縺吶°・溘阪・NG縲・,
                  '謾ｯ驟堺ｺｺ縺ｫ縺､縺ｪ縺後▲縺溘ｉ縲後♀譎る俣繧医ｍ縺励＞縺ｧ縺励ｇ縺・°・溘阪・NG・医・繝翫・蝠城｡鯉ｼ峨ゅ瑚・蜍輔メ繧ｧ繝・け繧､繝ｳ讖溘・莉ｶ縺ｧ縲阪→險縺｣縺滓凾轤ｹ縺ｧ闊亥袖縺ｪ縺代ｌ縺ｰ蛻・ｉ繧後ｋ縲・,
                  '豬∬｡後ｊ繝ｻ荳悶・荳ｭ縺ｮ豬√ｌ繧剃ｽｿ縺・ヨ繝ｼ繧ｯ・壹梧怙霑代ｈ縺上♀閠ｳ縺ｫ縺吶ｋ縺九→縺ｯ諤昴＞縺ｾ縺吶′縲阪悟・蝗ｽ縺九ｉ縺ｮ縺雁撫縺・粋繧上○縺悟悉蟷ｴ繧医ｊ縺九↑繧雁､壹￥縺ｪ縺｣縺ｦ縺阪※縺翫ｊ縺ｾ縺励※縲阪ｒ謖ｿ蜈･縲・,
                  '雉ｪ蝠上′縺ゅｋ・晁・蜻ｳ縺後≠繧九りｳｪ蝠上′縺ゅ▲縺溷・縺ｯ蜆ｪ蜈亥ｺｦ繧偵御ｸｭ縲阪∪縺溘・縲碁ｫ倥阪↓螟画峩縺吶ｋ縲・,
                  'info@螳帙・雉・侭騾∽ｻ假ｼ壻ｻｶ蜷阪↓縲後・・ｧ・閾ｪ蜍輔メ繧ｧ繝・け繧､繝ｳ讖溘・莉ｶ縲阪→蜈･蜉帙☆繧具ｼ医せ繝ｫ繝ｼ縺輔ｌ繧狗｢ｺ邇・′貂帙ｋ・峨・,
                  '雉・侭騾∽ｻ倥Γ繝ｼ繝ｫ縺ｫ鄂ｲ蜷阪→繧ｫ繧ｿ繝ｭ繧ｰ繧貞ｿ・★莉倥￠繧九ゅき繧ｿ繝ｭ繧ｰ縺ｮ豺ｻ莉俶ｼ上ｌ縺ｫ豕ｨ諢上・,
                  '繧ｷ繝ｪ繝ｳ繝繝ｼ骭蟇ｾ蠢懊↑縺ｩ縺ｮ蠑ｷ縺ｿ繧単R縺励※縺九ｉ雉・侭騾∽ｻ倥↓謖√▲縺ｦ縺・￥縲ゅ＞縺阪↑繧願ｳ・侭騾∽ｻ倥・NG縲・,
                  '縲後ゅ阪〒蛹ｺ蛻・ｋ縺ｪ縺ｩ縲∬ｩｱ縺玲婿繧偵ｆ縺｣縺上ｊ繧上°繧翫ｄ縺吶￥縲・,
                  '諡・ｽ楢・ｸ榊惠縺悟､壹＞蝣ｴ蜷医・繝輔Ο繝ｳ繝医↓雉・侭騾∽ｻ倥ｒ縺企｡倥＞縺吶ｋ縲・,
                  '邨・ｹ疲ｱｺ貂域｡井ｻｶ縺ｯ蠢・★蝣ｱ蜻翫ょ・繧雁哨縺後≠繧翫◎縺・↑繧蛾蝉ｸ蝣ｱ蜻翫・,
                  '雉・侭騾∽ｻ倥Γ繝ｼ繝ｫ縺ｮ髢句ｰ∫憾豕√ｒ遒ｺ隱阪る幕蟆∵ｭｴ縺ｪ縺冷・霑ｷ諠代Γ繝ｼ繝ｫ遒ｺ隱阪・繧｢繝峨Ξ繧ｹ遒ｺ隱阪・,
                  '驛ｨ螻区焚縺悟ｰ代↑縺・→縺薙ｍ縺ｫ縺ｯ繝ｫ繝ｼ繝繧ｿ繝悶Ξ繝・ヨ繝ｻ繧ｹ繝槭・繝医Ο繝・け繧ょ粋繧上○縺ｦ謠先｡医・,
                ].map((item, i) => (
                  <div key={i} className="flex gap-2 text-xs text-slate-300 bg-slate-700/30 rounded-lg p-3">
                    <span className="text-blue-400 font-bold flex-shrink-0">{i + 1}.</span>
                    <span>{item}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* 笏笏笏 TAB: 繝√ぉ繝・け繝ｪ繧ｹ繝・笏笏笏 */}
      {activeTab === 'checklist' && (
        <div className="space-y-6">
          <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
            <h2 className="text-base font-bold text-white mb-4">笨・譫ｶ髮ｻ讌ｭ蜍吶メ繧ｧ繝・け繝ｪ繧ｹ繝・/h2>
            <div className="space-y-2">
              {[
                '逋ｺ菫｡蜑阪↓諡・ｽ楢・ｒ閾ｪ蛻・・蜷榊燕縺ｫ螟画峩縺励◆縺・,
                '譫ｶ髮ｻ蠕後√せ繝・・繧ｸ繧呈ｭ｣縺励￥螟画峩縺励◆縺具ｼ井ｸ榊惠・乗妙繧奇ｼ乗悽遉ｾ縺ｸ・上け繝ｬ繝ｼ繝・丈ｻ也､ｾ陬ｽ蜩∽ｽｿ逕ｨ・・,
                '荳榊惠譎ゅ・縲後＞繧区凾髢灘ｸｯ繝ｻ譌･縲阪ｒ閨槭″縲√ち繧ｹ繧ｯ繧定ｨｭ螳壹＠縺溘°',
                '雉・侭騾∽ｻ俶凾・壹Γ繝ｼ繝ｫ繧｢繝峨Ξ繧ｹ繝ｻ蟋灘錐・医・・ｧ假ｼ峨・謳ｺ蟶ｯ逡ｪ蜿ｷ繧貞・蜉帙＠縺溘°',
                '雉・侭騾∽ｻ倥Γ繝ｼ繝ｫ縺ｫ鄂ｲ蜷阪→繧ｫ繧ｿ繝ｭ繧ｰ繧剃ｻ倥￠縺溘°',
                'info@螳帙・莉ｶ蜷阪↓縲後・・ｧ・閾ｪ蜍輔メ繧ｧ繝・け繧､繝ｳ讖溘・莉ｶ縲阪→蜈･繧後◆縺・,
                '莨夂､ｾ縺ｮ諡・ｽ楢・ｼ郁・蛻・錐・峨→繝ｪ繝ｼ繝峨せ繝・・繧ｿ繧ｹ繧貞､画峩縺励◆縺・,
                '雉・侭騾∽ｻ倥ち繧ｹ繧ｯ縺ｮ譛滄剞繧・騾ｱ髢灘ｾ後↓險ｭ螳壹＠縺溘°・医▽縺ｪ縺後ｊ繧・☆縺・凾髢灘ｸｯ繧り・・・・,
                '蜿嶺ｻ倥・諡・ｽ楢・・蜷榊燕繧剃ｸ｡譁ｹ閨槭＞縺溘°・医う繝ｳ繧ｻ繝ｳ譚｡莉ｶ・壹Γ繝｢縲先球蠖灘女莉伜・縺ｫ縲・酪縲醍ｭ会ｼ・,
                '雉ｪ蝠上′縺ゅ▲縺溷・縺ｯ蜆ｪ蜈亥ｺｦ繧偵御ｸｭ縲阪∪縺溘・縲碁ｫ倥阪↓螟画峩縺励◆縺・,
                '雉・侭騾∽ｻ伜ｾ・騾ｱ髢謎ｻ･蜀・↓蜀肴楔髮ｻ縺励◆縺・,
                '雉・侭騾∽ｻ倥Γ繝ｼ繝ｫ縺ｮ髢句ｰ∫憾豕√ｒ遒ｺ隱阪＠縺溘°',
                '縲檎┌莠ｺ縲阪→縺・≧繝ｯ繝ｼ繝峨ｒ菴ｿ縺｣縺ｦ縺・↑縺・°',
                '蛻・ｊ蜿｣繧・ｳｪ蝠上′縺ゅ▲縺滓｡井ｻｶ繧帝蝉ｸ蝣ｱ蜻翫＠縺溘°',
              ].map((item, i) => (
                <label key={i} className="flex items-start gap-3 p-3 bg-slate-700/40 rounded-xl cursor-pointer hover:bg-slate-700 transition-colors">
                  <input type="checkbox" className="w-4 h-4 accent-blue-500 mt-0.5 flex-shrink-0" />
                  <span className="text-sm text-slate-300">{item}</span>
                </label>
              ))}
            </div>
          </div>

          {/* 驥崎ｦ√・繧､繝ｳ繝域掠隕玖｡ｨ */}
          <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
            <h2 className="text-base font-bold text-white mb-4">東 驥崎ｦ√・繧､繝ｳ繝域掠隕玖｡ｨ</h2>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-slate-700">
                    <th className="text-left text-slate-400 font-medium py-2 pr-4 whitespace-nowrap">鬆・岼</th>
                    <th className="text-left text-white font-medium py-2">蜀・ｮｹ</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-700/50">
                  {[
                    { label: '蟇ｾ雎｡蜿門ｼ輔せ繝・・繧ｸ', value: '讌ｽ螟ｩ繝医Λ繝吶Ν・井ｸ榊惠・会ｼ医せ繝槭・繝医メ繧ｧ繝・け繧､繝ｳ・・, highlight: true },
                    { label: '霑ｽ蜉縺吶ｋ陦ｨ遉ｺ蛻・, value: '縲悟燕蝗槭・騾｣邨｡縲阪悟━蜈亥ｺｦ縲・ },
                    { label: '繧ｽ繝ｼ繝亥渕貅・, value: '縲悟燕蝗槭・騾｣邨｡縲肴律譎ゅ・譏・・ｼ磯℃蜴ｻ縺九ｉ・・ },
                    { label: '繧ｹ繧ｭ繝・・譚｡莉ｶ', value: '蜆ｪ蜈亥ｺｦ縺後碁ｫ倥阪∪縺溘・縲御ｸｭ縲阪・繝ｬ繧ｳ繝ｼ繝・, highlight: true },
                    { label: '譫ｶ髮ｻ鬆・ｺ・, value: '繝ｪ繧ｹ繝医・荳翫°繧蛾・分' },
                    { label: '譫ｶ髮ｻ蜑阪・蠢・井ｽ懈･ｭ', value: '蜿門ｼ墓球蠖楢・ｒ閾ｪ蛻・・蜷榊燕縺ｫ螟画峩・遺・邨ｶ蟇ｾ蠢倥ｌ縺壹↓・・, highlight: true },
                    { label: '譫ｶ髮ｻ蠕後・菴懈･ｭ', value: '蜿門ｼ輔せ繝・・繧ｸ繧堤ｵ先棡縺ｫ蠢懊§縺ｦ譖ｴ譁ｰ' },
                    { label: '繧ｻ繝溘リ繝ｼ髢句ぎ譌･', value: '豌ｴ譖・1:00縲・・・驥第屆13:00縲懶ｼ・OOM・・, highlight: true },
                    { label: '繧､繝ｳ繧ｻ繝ｳ譚｡莉ｶ', value: '蜿嶺ｻ倥・諡・ｽ楢・・蜷榊燕繧剃ｸ｡譁ｹ閨槭￠縺ｦ100蜀・ },
                  ].map((row, i) => (
                    <tr key={i}>
                      <td className="text-slate-400 py-3 pr-4 whitespace-nowrap font-medium">{row.label}</td>
                      <td className={`py-3 ${row.highlight ? 'text-yellow-300 font-medium' : 'text-slate-300'}`}>{row.value}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* 笏笏笏 TAB: 繝｡繝ｼ繝ｫ繝・Φ繝励Ξ 笏笏笏 */}
      {activeTab === 'mail' && (
        <div className="space-y-6">
          {[
            {
              key: 'zoom',
              title: '套 ZOOM繝溘・繝・ぅ繝ｳ繧ｰ譯亥・繝｡繝ｼ繝ｫ',
              content: `縺贋ｸ冶ｩｱ縺ｫ縺ｪ縺｣縺ｦ縺翫ｊ縺ｾ縺吶・(譬ｪ)繝・ヰ繧､繧ｹ繧ｨ繝ｼ繧ｸ繧ｧ繝ｳ繧ｷ繝ｼ縺ｮ縲・・〒縺斐＊縺・∪縺吶・縺頑遠縺｡蜷医ｏ縺帙・縺頑凾髢薙ｒ縺・◆縺縺代∪縺吶％縺ｨ縲∵─隰晉筏縺嶺ｸ翫￡縺ｾ縺吶・讓呵ｨ倥・莉ｶ縺ｫ縺､縺阪∪縺励※縲∽ｸ玖ｨ倥・縺ｨ縺翫ｊWeb繝溘・繝・ぅ繝ｳ繧ｰ・・OOM・峨ｒ縺疲｡亥・逕ｳ縺嶺ｸ翫￡縺ｾ縺吶・
險・譌･譎ゑｼ・026蟷ｴ縲・怦縲・律・医・ｼ峨・・ｼ・0・・蠖｢蠑擾ｼ壹が繝ｳ繝ｩ繧､繝ｳ・・OOM・・ZOOM蜈･螳､URL・喇ttps://us06web.zoom.us/j/84410321175?pwd=YklablhmOGIwQ0tCQmJXN0hnak9UZz09
窶ｻ蠖捺律縺ｯ縺頑凾髢薙↓縺ｪ繧翫∪縺励◆繧峨∽ｸ願ｨ篭RL繧医ｊ縺泌・螳､繧偵♀鬘倥＞縺・◆縺励∪縺吶・縺泌､壼ｿ吶・謚倥∵＄邵ｮ縺ｧ縺ｯ縺斐＊縺・∪縺吶′縲∝ｽ捺律縺ｯ菴募穀繧医ｍ縺励￥縺企｡倥＞逕ｳ縺嶺ｸ翫￡縺ｾ縺吶Ａ,
            },
            {
              key: 'checkin',
              title: '透 雉・侭騾∽ｻ倥Γ繝ｼ繝ｫ・医メ繧ｧ繝・け繧､繝ｳ讖滂ｼ・,
              content: `謾ｯ驟堺ｺｺ 讒・
縺贋ｸ冶ｩｱ縺ｫ縺ｪ繧翫∪縺吶・譛ｬ譌･縺ｯ閾ｪ蜍輔メ繧ｧ繝・け繧､繝ｳ讖溘・莉ｶ縺ｧ縺企崕隧ｱ縺ゅｊ縺後→縺・＃縺悶＞縺ｾ縺励◆縲・莉雁ｾ後・繧､繝ｳ繝舌え繝ｳ繝牙ｯｾ遲悶ｄ縲∽ｺｺ謇倶ｸ崎ｶｳ縲∝茜逶顔紫蜷台ｸ翫∵･ｭ蜍吝柑邇・喧縺ｮ髱｢縺ｧ螟ｧ螟芽憶縺・ｩ穂ｾ｡繧偵＞縺溘□縺・※縺翫ｊ縺ｾ縺吶・縺ｾ縺溘∽ｾ｡譬ｼ髱｢縺ｫ縺､縺阪∪縺励※繧ら嚀讒倥↓螟ｧ螟峨＃螂ｽ隧輔ｒ縺・◆縺縺・※縺翫ｊ縺ｾ縺吶・
笳丈ｺｺ謇倶ｸ崎ｶｳ繝ｻ讌ｭ蜍吝柑邇・喧蟇ｾ遲・繝輔Ο繝ｳ繝医・莠ｺ蜩｡蜑頑ｸ帙∫┌莠ｺ蛹悶′蜿ｯ閭ｽ縺ｫ縲ゅせ繧ｿ繝・ヵ縺ｮ讌ｭ蜍呵ｲ諡・・霆ｽ貂帚∑縺雁ｮ｢讒倥・繧ｹ繝医Ξ繧ｹ邱ｩ蜥・
笳上き繝ｼ繝峨く繝ｼ莉･螟悶↓繧ょｯｾ蠢・繝ｫ繝ｼ繝繧ｫ繝ｼ繝峨く繝ｼ莉･螟悶↓繧ゅ√せ繝槭・繝医Ο繝・け繧・黄逅・く繝ｼ・医す繝ｪ繝ｳ繝繝ｼ骭・峨↓繧ょｯｾ蠢懷庄閭ｽ縺ｧ縺吶ゑｼ医が繝励す繝ｧ繝ｳ繧ｭ繝ｼ繝懊ャ繧ｯ繧ｹ縺ｮ菴ｵ逕ｨ・・
笳上・繧ｹ繝斐ち繝ｪ繝・ぅ繝ｼ縺ｮ蜷台ｸ・莠句燕繝√ぉ繝・け繧､繝ｳ繧ｷ繧ｹ繝・Β縺ｪ縺ｩ繧貞茜逕ｨ縺吶ｋ縺薙→縺ｧ縲√ヵ繝ｭ繝ｳ繝医〒縺ｮ莠句漁逧・が繝壹Ξ繝ｼ繧ｷ繝ｧ繝ｳ繧貞炎貂帚∑縺雁ｮ｢讒倥→縺ｮ蟇ｾ隧ｱ譎る俣縺悟｢励∴縲・､ｨ蜀・命險ｭ繧・ｦｳ蜈画｡亥・縺ｪ縺ｩ縺ｮ謗･螳｢繧ｵ繝ｼ繝薙せ繧偵ｈ繧贋ｸ螻､謇句字縺剰｡後≧縺薙→縺悟庄閭ｽ縺ｫ縲・
笳丞､夂ｨｮ螟壽ｧ倥↑繧ｫ繧ｹ繧ｿ繝槭う繧ｺ
譛晞｣溷虻縺ｮ逋ｺ陦後ｄ譌･蟶ｰ繧頑ｸｩ豕牙ｮ｢縺ｮ蜿嶺ｻ倥・貂・ｮ励↑縺ｩ縺ｮ繝・う繝ｦ繝ｼ繧ｹ讖溯・縺ｫ蜉縺医∵命險ｭ縺ｮ繝九・繧ｺ縺ｫ蠢懊§縺ｦ讒倥・↑繧ｫ繧ｹ繧ｿ繝槭う繧ｺ縺ｫ蜿悶ｊ邨・ｓ縺ｧ縺・∪縺吶・
笳上う繝ｳ繝舌え繝ｳ繝牙ｯｾ蠢・螟門嵜隱槫ｯｾ蠢懶ｼ・3繝ｵ蝗ｽ隱橸ｼ峨ゅヱ繧ｹ繝昴・繝医せ繧ｭ繝｣繝ｳ縲∵悽莠ｺ遒ｺ隱阪ｂ蜿ｯ閭ｽ縺ｧ縺吶・
縲仙・譛溯ｲｻ逕ｨ縺ｫ縺､縺・※縲・AdvaNceD IoT 繝√ぉ繝・け繧､繝ｳ遲蝉ｽ楢ｲｻ逕ｨ・句・譛溯ｨｭ螳夊ｲｻ逕ｨ竊棚T陬懷勧驥第ｴｻ逕ｨ縺ｧ1,330,000蜀・ｽ・窶ｻ繧ｷ繝ｪ繝ｳ繝繝ｼ骭縺ｫ繧ょｯｾ蠢懷庄閭ｽ縺ｧ縺吶・窶ｻ蟆剰ｦ乗ｨ｡蜷代￠繧ｿ繝悶Ξ繝・ヨ蝙九・1蜿ｰ邏・6荳・・・槭〒蟆主・蜿ｯ閭ｽ縲・
縲先怦鬘崎ｲｻ逕ｨ縺ｫ縺､縺・※縲・繝ｻ菴ｿ逕ｨ縺励↑縺・怦縺ｯ0蜀・↓縺ｪ繧翫∪縺吶ゑｼ亥ｭ｣遽髯仙ｮ夂音蛻･譁咎≡蟶ｯ・・繝ｻ繝ｫ繝ｼ繝蛻ｩ逕ｨ譁呻ｼ暗鈴Κ螻区焚1・・0螳､縺ｾ縺ｧ・我ｸ驛ｨ螻凝・00蜀・繝ｻ3蟷ｴ逶ｮ莉･髯阪・繝ｫ繝ｼ繝蛻ｩ逕ｨ譁・00蜀・鈴Κ螻区焚

窶ｻ蝠・刀縺ｮ隱ｬ譏惹ｼ壹そ繝溘リ繝ｼ繧ゅが繝ｳ繝ｩ繧､繝ｳ縺ｧ豈朱ｱ2蝗樣幕蛯ｬ縺励※縺翫ｊ縺ｾ縺吶ゑｼ・譎る俣遞句ｺｦ・・繝ｻ豌ｴ譖懈律・・1・・0・・繝ｻ驥第屆譌･・・3・・0・・縺泌ｸ梧悍縺ｮ譌･譎ゅ′縺斐＊縺・∪縺励◆繧峨√＃霑比ｿ｡縺上□縺輔＞縲・
WEB迚医・縺薙■繧峨〒縺吶窟dvaNceD IoT 繧ｹ繝槭・繝医メ繧ｧ繝・け繧､繝ｳ縲・https://and-iot.jp/dms-cardlock`,
            },
            {
              key: 'tablet',
              title: '透 繝ｫ繝ｼ繝繧ｿ繝悶Ξ繝・ヨ雉・侭騾∽ｻ倥Γ繝ｼ繝ｫ',
              content: `縺贋ｸ冶ｩｱ縺ｫ縺ｪ縺｣縺ｦ縺翫ｊ縺ｾ縺吶ゅョ繝舌う繧ｹ繧ｨ繝ｼ繧ｸ繧ｧ繝ｳ繧ｷ繝ｼ讖区悽縺ｧ縺斐＊縺・∪縺吶・蜈医⊇縺ｩ縺ｮ縺願ｩｱ縺ｧ繝ｫ繝ｼ繝繧ｿ繝悶Ξ繝・ヨ・亥・邱夐崕隧ｱ・峨・雉・侭繧偵♀騾√ｊ縺励∪縺吶・
繝ｫ繝ｼ繝繧ｿ繝悶Ξ繝・ヨ縺ｯ縲√け繝ｩ繧ｦ繝峨す繧ｹ繝・Β縺ｮ繧ｻ繝・ヨ縺ｧ縺吶る°蝟ｶ縺ｮ蜉ｹ邇・喧縺ｨ繧ｳ繧ｹ繝亥炎貂帙ｒ螳溽樟縺ｧ縺阪∪縺吶・
繝｡繝ｪ繝・ヨ・・繝ｻ繧ｹ繧ｿ繝・ヵ縺ｮ譁ｹ縺後ヵ繝ｭ繝ｳ繝医°繧蛾屬繧後※縺・※繧ゅ∫ｧｻ蜍輔＠縺ｪ縺後ｉ蟇ｾ蠢懊〒縺阪∪縺吶・繝ｻ繧ｲ繧ｹ繝域ｧ倥°繧峨・逹菫｡縺御ｸ逶ｮ縺ｧ繧上°繧翫∪縺吶ゑｼ井ｾ具ｼ壹・05縺ｮ逕ｰ荳ｭ讒倥阪→陦ｨ遉ｺ・・繝ｻ螟夊ｨ隱櫁｡ｨ遉ｺ縺悟庄閭ｽ縺ｧ縲√う繝ｳ繝舌え繝ｳ繝牙ｯｾ遲悶↓繧ゅ・繝ｻ螳ｿ豕企未騾｣縺ｮ諠・ｱ繧貞・縺ｦ繧ｿ繝悶Ξ繝・ヨ縺ｫ髮・ｴ・〒縺阪√・繝ｼ繝代・繝ｬ繧ｹ蛹悶′蜿ｯ閭ｽ縲・繝ｻ繧ｿ繝悶Ξ繝・ヨ繧・せ繝槭・縺ｮ遶ｯ譛ｫ蛻晄悄雋ｻ逕ｨ縺ｯ0蜀・ｼ医す繧ｹ繝・Β蛻晄悄雋ｻ逕ｨ100,000蜀・ｼ狗ｫｯ譛ｫ逋ｻ骭ｲ雋ｻ逕ｨ1蜿ｰ19,800蜀・′蛻･騾費ｼ峨・繝ｻ譛磯｡肴侭驥代・1螳､100蜀・・T陬懷勧驥第ｴｻ逕ｨ縺ｧ蠕｡遉ｾ雋諡・′譛磯｡崎ｲｻ逕ｨ繧ょ性繧∫ｴ・/3縺ｫ縲・
蠑顔､ｾ縺ｧ縺ｯ莉悶↓繧ゅ・繝・Ν譁ｽ險ｭ蜷代￠縺ｮ閾ｪ遉ｾ髢狗匱陬ｽ蜩√ｒ謠蝉ｾ帙＠縺ｦ縺翫ｊ縺ｾ縺吶・https://and-iot.jp/`,
            },
            {
              key: 'sign',
              title: '笨搾ｸ・鄂ｲ蜷阪ユ繝ｳ繝励Ξ繝ｼ繝・,
              content: `笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏・縺贋ｸ冶ｩｱ縺ｫ縺ｪ縺｣縺ｦ縺翫ｊ縺ｾ縺吶・譬ｪ蠑丈ｼ夂､ｾ繝・ヰ繧､繧ｹ繧ｨ繝ｼ繧ｸ繧ｧ繝ｳ繧ｷ繝ｼ 縲・・・縲・50-0015
螟ｧ髦ｪ蟶り･ｿ蛹ｺ蜊怜豎・-17-18 蜴溽伐繝薙Ν繝・ぅ繝ｳ繧ｰ1F
TEL:06-6585-9865 FAX:06-6585-9875
Email: ・郁・蛻・・繧｢繝峨Ξ繧ｹ・・DA   www.device-agency.co.jp
笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏～,
            },
          ].map(tpl => (
            <div key={tpl.key} className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-base font-bold text-white">{tpl.title}</h2>
                <button
                  onClick={() => copy(tpl.content, tpl.key)}
                  className={`px-4 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                    copiedKey === tpl.key
                      ? 'bg-green-600 text-white'
                      : 'bg-slate-700 hover:bg-slate-600 text-slate-300'
                  }`}
                >
                  {copiedKey === tpl.key ? '笨・繧ｳ繝斐・貂医∩' : '搭 繧ｳ繝斐・'}
                </button>
              </div>
              <pre className="text-xs text-slate-300 bg-slate-900 rounded-xl p-4 whitespace-pre-wrap leading-relaxed max-h-64 overflow-y-auto">{tpl.content}</pre>
            </div>
          ))}

          {/* Zoom Phone騾｣謳ｺ */}
          <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
            <h2 className="text-base font-bold text-white mb-4">導 Zoom Phone ﾃ・HubSpot 騾｣謳ｺ謇矩・/h2>
            <div className="space-y-2">
              {[
                'HubSpot縺ｫ繝ｭ繧ｰ繧､繝ｳ竊偵・繝ｼ繧ｱ繝・ヨ繝励Ξ繧､繧ｹ・亥ｮｶ繧｢繧､繧ｳ繝ｳ・峨ｒ髢九￥',
                '縲兄oom縲阪〒讀懃ｴ｢竊偵兄oom Phone for HubSpot縲坂・縲後い繝励Μ繧偵う繝ｳ繧ｹ繝医・繝ｫ縲・,
                'Zoom Web繝昴・繧ｿ繝ｫ縺ｮ繝ｭ繧ｰ繧､繝ｳ逕ｻ髱｢縺ｧZoomPhone縺梧怏蜉ｹ縺ｪID縺ｧ繝ｭ繧ｰ繧､繝ｳ',
                '縲梧ｪ蠑丈ｼ夂､ｾ繝・ヰ繧､繧ｹ繧ｨ繝ｼ繧ｸ繧ｧ繝ｳ繧ｷ繝ｼ縲阪ｒ繝槭・繧ｯ竊偵後い繧ｫ繧ｦ繝ｳ繝磯∈謚槭・,
                '繝√ぉ繝・け繝懊ャ繧ｯ繧ｹ縺ｫ繝√ぉ繝・け竊偵後い繝励Μ繧呈磁邯壹坂・縲靴onfirm縲坂・縲檎｢ｺ隱阪☆繧九・,
                '縲後し繧､繝ｳ繧､繝ｳ縺ｫ謌仙粥縺励∪縺励◆縲阪→陦ｨ遉ｺ縺輔ｌ繧後・螳御ｺ・,
                '笘・㍾隕・ｼ啝oom Web繝昴・繧ｿ繝ｫ竊帝崕隧ｱ竊定ｨｭ螳壺・逋ｺ菫｡閠・D・育┌莠ｺ繝√ぉ繝・け繧､繝ｳ蝟ｶ讌ｭ・峨ｒ驕ｸ謚・,
              ].map((item, i) => (
                <div key={i} className="flex gap-3 text-sm text-slate-300 bg-slate-700/40 rounded-lg p-3">
                  <span className="w-5 h-5 bg-blue-600 rounded-full flex items-center justify-center text-xs font-bold text-white flex-shrink-0">{i + 1}</span>
                  {item}
                </div>
              ))}
            </div>
            <div className="mt-4 bg-yellow-950/50 border border-yellow-800/50 rounded-xl p-4">
              <p className="text-sm font-bold text-yellow-400 mb-2">笞・・騾｣謳ｺ縺後≧縺ｾ縺上＞縺九↑縺・ｴ蜷・/p>
              <ul className="text-sm text-slate-300 space-y-1">
                <li>繝ｻZOOM繝ｯ繝ｼ繧ｯ繝励Ξ繧､繧ｹ繧偵し繧､繝ｳ繧｢繧ｦ繝遺・繧ｵ繧､繝ｳ繧､繝ｳ縺礼峩縺・/li>
                <li>繝ｻHubSpot縺ｮ繧ｳ繝ｼ繝ｫ繧ゅし繧､繝ｳ繧｢繧ｦ繝遺・繧ｵ繧､繝ｳ繧､繝ｳ縺礼峩縺・/li>
                <li>繝ｻHubSpot荳企Κ縺ｮ髮ｻ隧ｱ繝槭・繧ｯ繧｢繧､繧ｳ繝ｳ縺九ｉ繧ｵ繧､繝ｳ繧､繝ｳ竊貞挨繧ｿ繝悶〒縲兄OOM繝輔か繝ｳ縲埼∈謚樞・Google縺ｧ繝ｭ繧ｰ繧､繝ｳ</li>
              </ul>
            </div>
          </div>
        </div>
      )}

      {/* 蜿り・ｳ・侭繝ｪ繝ｳ繧ｯ */}
      <div className="mt-6 bg-slate-800 rounded-2xl border border-slate-700 p-5">
        <p className="text-xs text-slate-400 font-medium mb-3">刀 蜿り・ｳ・侭</p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          <a href="https://app-na2.hubspot.com/contacts/39705134/objects/0-3/views/353515006/list" target="_blank" rel="noopener noreferrer"
            className="flex items-center gap-3 p-3 bg-orange-900/30 hover:bg-orange-900/50 border border-orange-800/50 rounded-xl transition-colors group">
            <span className="text-lg">泛</span>
            <div>
              <p className="text-white text-xs font-medium group-hover:text-orange-300 transition-colors">HubSpot 譫ｶ髮ｻ繝ｪ繧ｹ繝・/p>
              <p className="text-slate-500 text-xs">蜿門ｼ穂ｸ隕ｧ・域･ｽ螟ｩ繝医Λ繝吶Ν繝輔ぅ繝ｫ繧ｿ繝ｼ貂茨ｼ・/p>
            </div>
          </a>
          <a href="https://us02web.zoom.us/myhome" target="_blank" rel="noopener noreferrer"
            className="flex items-center gap-3 p-3 bg-blue-900/30 hover:bg-blue-900/50 border border-blue-800/50 rounded-xl transition-colors group">
            <span className="text-lg">道</span>
            <div>
              <p className="text-white text-xs font-medium group-hover:text-blue-300 transition-colors">Zoom 繝槭う繝帙・繝</p>
              <p className="text-slate-500 text-xs">譫ｶ髮ｻ繝ｻ繧ｻ繝溘リ繝ｼ逕ｨ Zoom</p>
            </div>
          </a>
          <a href="https://docs.google.com/spreadsheets/d/1F2ycU3glbgrJCOkLRKHg86ROWggkbYOZXxhA2vco84o/edit?gid=767829959#gid=767829959" target="_blank" rel="noopener noreferrer"
            className="flex items-center gap-3 p-3 bg-slate-700/50 hover:bg-slate-700 rounded-xl transition-colors group">
            <span className="text-lg">投</span>
            <div>
              <p className="text-white text-xs font-medium group-hover:text-blue-300 transition-colors">繝・Ξ繧｢繝晄･ｭ蜍吶・繝九Η繧｢繝ｫ・医せ繝励Ξ繝・ラ繧ｷ繝ｼ繝茨ｼ・/p>
              <p className="text-slate-500 text-xs">繝・Ξ繧｢繝晄･ｭ蜍吶・繝九Η繧｢繝ｫ謾ｹ豁｣繧ｷ繝ｼ繝・/p>
            </div>
          </a>
          <a href="https://docs.google.com/spreadsheets/d/1WnwEhp2Db9lDHNw8qp_h2ZjhMY-mZG9TXcAAh6RX59w/edit?gid=1927965581#gid=1927965581" target="_blank" rel="noopener noreferrer"
            className="flex items-center gap-3 p-3 bg-slate-700/50 hover:bg-slate-700 rounded-xl transition-colors group">
            <span className="text-lg">搭</span>
            <div>
              <p className="text-white text-xs font-medium group-hover:text-blue-300 transition-colors">繧｢繧ｦ繝医ヰ繧ｦ繝ｳ繝臥ｮ｡逅・ｰｿ</p>
              <p className="text-slate-500 text-xs">縲舌せ繝槭・繝医メ繧ｧ繝・け繧､繝ｳ縲第楔髮ｻ邂｡逅・/p>
            </div>
          </a>
        </div>
      </div>
    </div>
  )
}
