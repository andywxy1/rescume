// Basic Resume Template for Rescume v2.0
// Clean, ATS-friendly single-column design
// Font size is adjustable for auto-fit functionality

#let resume(
  // Font size parameter for auto-fit
  font-size: 11pt,

  // Header data
  name: "John Doe",
  location: none,
  email: none,
  phone: none,
  linkedin: none,
  github: none,
  website: none,

  // Content sections (passed as data structure)
  summary: none,
  education: (),
  experience: (),
  projects: (),
  skills: none,
) = {

  // Page setup - US Letter, standard margins
  set page(
    paper: "us-letter",
    margin: (x: 0.75in, y: 0.75in)
  )

  // Text defaults - using adjustable font size
  set text(
    font: ("New Computer Modern", "Latin Modern Roman", "Times New Roman"),
    size: font-size,
    fallback: true
  )

  // Paragraph spacing
  set par(justify: false, leading: 0.65em)

  // Heading styles
  show heading.where(level: 1): it => {
    set text(size: font-size * 1.2, weight: "bold")
    upper(it.body)
    v(0.3em)
    line(length: 100%, stroke: 0.5pt)
    v(0.5em)
  }

  show heading.where(level: 2): it => {
    set text(size: font-size * 1.0, weight: "bold")
    it
    v(0.3em)
  }

  // === HEADER ===
  align(center)[
    #text(size: font-size * 1.8, weight: "bold")[#name]
    #v(0.4em)

    #text(size: font-size * 0.9)[
      #if location != none [ #location ]
      #if email != none [
        #if location != none [ | ]
        #link("mailto:" + email)[#email]
      ]
      #if phone != none [
        #if email != none or location != none [ | ]
        #phone
      ]
      #linebreak()
      #if linkedin != none [
        #link("https://" + linkedin)[#linkedin]
      ]
      #if github != none [
        #if linkedin != none [ | ]
        #link("https://" + github)[#github]
      ]
      #if website != none [
        #if linkedin != none or github != none [ | ]
        #link("https://" + website)[#website]
      ]
    ]
  ]

  v(0.8em)

  // === SUMMARY (Optional) ===
  if summary != none [
    #text(style: "italic", size: font-size * 0.95)[#summary]
    #v(0.6em)
  ]

  // === EDUCATION ===
  if education.len() > 0 [
    = Education

    #for edu in education [
      *#edu.institution* #h(1fr) #edu.dates \
      #if "degree" in edu [
        #edu.degree
        #if "gpa" in edu and edu.gpa != none [ | GPA: #edu.gpa ]
        \
      ]
      #if "details" in edu and edu.details.len() > 0 [
        #for detail in edu.details [
          - #detail
        ]
      ]
      #v(0.4em)
    ]
  ]

  // === EXPERIENCE ===
  if experience.len() > 0 [
    = Professional Experience

    #for exp in experience [
      *#exp.role* | #exp.company
      #if "location" in exp [ | #exp.location ]
      #h(1fr) #exp.dates \
      #v(0.2em)

      #for bullet in exp.bullets [
        - #bullet
      ]
      #v(0.4em)
    ]
  ]

  // === PROJECTS ===
  if projects.len() > 0 [
    = Projects

    #for proj in projects [
      *#proj.name*
      #if "subtitle" in proj [ | #proj.subtitle ]
      #if "dates" in proj [ #h(1fr) #proj.dates ]
      \
      #v(0.2em)

      #for bullet in proj.bullets [
        - #bullet
      ]
      #v(0.4em)
    ]
  ]

  // === SKILLS ===
  if skills != none [
    = Technical Skills

    #if "languages" in skills and skills.languages.len() > 0 [
      *Languages:* #skills.languages.join(", ") \
    ]
    #if "frameworks" in skills and skills.frameworks.len() > 0 [
      *Frameworks:* #skills.frameworks.join(", ") \
    ]
    #if "tools" in skills and skills.tools.len() > 0 [
      *Tools:* #skills.tools.join(", ") \
    ]
    #if "concepts" in skills and skills.concepts.len() > 0 [
      *Concepts:* #skills.concepts.join(", ")
    ]
  ]
}

// Example usage (for testing - will be replaced with actual data)
#resume(
  font-size: 11pt,
  name: "Sample User",
  email: "sample@example.com",
  phone: "(555) 123-4567",
  location: "San Francisco, CA",
  linkedin: "linkedin.com/in/sample",
  github: "github.com/sample",

  education: (
    (
      institution: "Example University",
      degree: "B.S. in Computer Science",
      dates: "2018 - 2022",
      gpa: "3.8/4.0",
      details: ("Relevant coursework: Data Structures, Algorithms, Machine Learning")
    ),
  ),

  experience: (
    (
      company: "Tech Company",
      role: "Software Engineer",
      location: "Remote",
      dates: "2022 - Present",
      bullets: (
        "Built scalable microservices serving 1M+ users",
        "Improved system performance by 40% through optimization",
        "Led team of 3 engineers in developing new features"
      )
    ),
  ),

  skills: (
    languages: ("Python", "JavaScript", "SQL"),
    frameworks: ("React", "Django", "FastAPI"),
    tools: ("Git", "Docker", "AWS"),
    concepts: ("Agile", "CI/CD", "REST APIs")
  )
)
