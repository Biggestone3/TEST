import { News } from './News';
import image from '../assets/image.png'
const newsItemsByLang: { [key: string]: News[] } = {
  en: [
    new News(
      "Quantum Computing Breakthrough Achieved at MIT Labs",
      `Researchers at MIT have successfully demonstrated error correction in a 72-qubit quantum processor, 
      marking a significant milestone in stable quantum computations.\n
      The team achieved 99.9% gate fidelity using novel superconducting circuits cooled to near absolute zero. 
      This breakthrough could accelerate practical applications in pharmaceutical research and climate modeling.`,
      image,
      `Lead researcher Dr. Alicia Torres explained: "Our error-correction protocol maintains quantum coherence 
      10x longer than previous attempts. This brings us closer to fault-tolerant quantum computing that could 
      revolutionize fields from cryptography to materials science."\n
      The next phase will focus on scaling to 1000+ qubits while maintaining error rates. Industry partners 
      including IBM and Google Quantum AI have expressed interest in collaborating on commercialization efforts.`,
      [
        { name: "MIT News Office", url: "https://news.mit.edu" },
        { name: "Nature Quantum", url: "https://nature.com/quantum" },
        { name: "IEEE Spectrum", url: "https://spectrum.ieee.org" },
        { name: "Quantum Tech Journal", url: "https://quantumtechjournal.org" }
      ],
      new Date(Date.now() - 45 * 60 * 1000) // 45 minutes ago
    ),
    new News(
      "Global Climate Accord: 2030 Emissions Targets Revised",
      `193 countries agree to accelerate carbon neutrality goals at UN Climate Summit, 
      bringing forward emissions reduction targets by 5 years.\n
      New commitments include phasing out coal power by 2035 in developed nations and 
      establishing a $100B/year climate adaptation fund for developing countries.`,
      image,
      `UN Secretary-General António Guterres stated: "This revised timeline reflects the 
      urgent reality of our climate crisis. We're seeing concrete commitments to triple 
      renewable energy capacity and implement carbon pricing mechanisms."\n
      Key measures include:\n- 50% reduction in methane emissions by 2030\n- Global EV sales 
      mandate of 60% by 2035\n- $75/ton minimum carbon price for G20 nations`,
      [
        { name: "UN Climate Report", url: "https://unfccc.int" },
        { name: "IPCC Data Portal", url: "https://ipcc.ch" },
        { name: "Climate Watch", url: "https://climatewatch.org" },
        { name: "Renewables Now", url: "https://renewablesnow.com" }
      ],
      new Date(Date.now() - 2 * 60 * 60 * 1000) // 2 hours ago
    ),
    new News(
      "NASA's Lunar Gateway Station Enters Construction Phase",
      `International consortium begins assembly of first permanent lunar space station, 
      marking a new era in space exploration.\n
      The Gateway will serve as a staging point for Artemis missions and deep space exploration, 
      with initial modules launching in 2025.`,
      "https://images.unsplash.com/photo-1454789548928-9efd52dc4031",
      `Gateway Program Manager Sarah Johnson revealed: "We're using revolutionary 3D-printing 
      techniques with lunar regolith to construct 40% of station components in situ."\n
      Key features:\n- Radiation-shielded habitation module\n- Lunar lander docking system\n
      - Deep space communications array\n- Scientific research laboratories`,
      [
        { name: "NASA Artemis", url: "https://nasa.gov/artemis" },
        { name: "ESA Gateway", url: "https://esa.int/gateway" },
        { name: "SpaceNews", url: "https://spacenews.com" },
        { name: "Lunar Exploration", url: "https://lunar.org" }
      ],
      new Date(Date.now() - 90 * 60 * 1000) // 1.5 hours ago
    )
  ],
  ar: [
    new News(
      "اختراق علمي في الحوسبة الكمومية بمعهد ماساتشوستس",
      `تمكن باحثون في معهد ماساتشوستس للتكنولوجيا من تحقيق تقدم كبير في تصحيح الأخطاء 
      في معالج كمي مكون من 72 كيوبت، مما يمثل خطوة هامة نحو الحوسبة الكمومية المستقرة.\n
      حقق الفريق دقة بنسبة 99.9% باستخدام دارات فائقة التوصيل مبردة إلى درجات قريبة من الصفر المطلق. 
      هذا الإنجاز قد يسرع التطبيقات العملية في مجالات البحث الدوائي ونمذجة المناخ.`,
      image,
      `أوضحت الدكتورة أليسيا توريس، الباحثة الرئيسية: "بروتوكولنا الجديد يحافظ على التماسك الكمي 
      لمدة أطول بعشر مرات من المحاولات السابقة. هذا يقربنا من حوسبة كمومية مقاومة للأخطاء 
      يمكنها إحداث ثورة في مجالات من التشفير إلى علوم المواد."\n
      المرحلة القادمة ستركز على زيادة عدد الكيوبتات إلى أكثر من 1000 مع الحفاظ على معدلات الأخطاء المنخفضة.`,
      [
        { name: "أخبار معهد ماساتشوستس", url: "https://news.mit.edu" },
        { name: "نيتشر للكموميات", url: "https://nature.com/quantum" },
        { name: "مجلة آي تربل إي", url: "https://spectrum.ieee.org" },
        { name: "مجلة التكنولوجيا الكمومية", url: "https://quantumtechjournal.org" }
      ],
      new Date(Date.now() - 45 * 60 * 1000) // 45 minutes ago
    ),
    new News(
      "اتفاقية عالمية جديدة لخفض الانبعاثات بحلول 2030",
      `وافقت 193 دولة على تسريع أهداف الحياد الكربوني في قمة المناخ الأممية، 
      مع تقديم مواعيد خفض الانبعاثات خمس سنوات.\n
      تشمل الالتزامات الجديدة التخلص التدريجي من طاقة الفحم بحلول 2035 في الدول المتقدمة 
      وإنشاء صندوق تكيف مناخي بقيمة 100 مليار دولار سنويًا للدول النامية.`,
      image,
      `صرح الأمين العام للأمم المتحدة أنطونيو غوتيريش: "يعكس هذا الجدول الزمني 
      الحالة الطارئة لأزمة المناخ. نرى التزامات ملموسة لزيادة قدرة الطاقة المتجددة 
      ثلاث مرات وتنفيذ آليات تسعير الكربون."\n
      تشمل الإجراءات الرئيسية:\n- خفض انبعاثات الميثان بنسبة 50% بحلول 2030\n- فرض 
      بيع 60% من السيارات الكهربائية عالميًا بحلول 2035\n- سعر كربون أدنى 75 دولارًا للطن في دول مجموعة العشرين`,
      [
        { name: "تقرير الأمم المتحدة للمناخ", url: "https://unfccc.int" },
        { name: "بوابة بيانات الهيئة الحكومية", url: "https://ipcc.ch" },
        { name: "مراقبة المناخ", url: "https://climatewatch.org" },
        { name: "الطاقات المتجددة الآن", url: "https://renewablesnow.com" }
      ],
      new Date(Date.now() - 2 * 60 * 60 * 1000) // 2 hours ago
    )
  ]
};

export default newsItemsByLang;