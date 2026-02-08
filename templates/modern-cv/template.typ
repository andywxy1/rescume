// Rescume Template: Modern CV
// Based on modern-cv package v0.9.0
// Colorful, modern design with accent colors

#import "@preview/modern-cv:0.9.0": *

// Auto-fit function for Modern CV template
#let auto-fit-resume(
  data,
  min-font-size: 9pt,
  default-font-size: 10pt,
  accent-color: rgb("#26428b")
) = {
  // Estimate font size based on content volume
  let total-bullets = 0
  if "experience" in data {
    for exp in data.experience {
      if "bullets" in exp {
        total-bullets = total-bullets + exp.bullets.len()
      }
    }
  }
  if "projects" in data and data.projects != none {
    for proj in data.projects {
      if "bullets" in proj {
        total-bullets = total-bullets + proj.bullets.len()
      }
    }
  }

  // Adjust font size based on content
  let estimated-size = default-font-size
  if total-bullets > 20 {
    estimated-size = 9pt
  } else if total-bullets > 15 {
    estimated-size = 9.5pt
  }

  if estimated-size < min-font-size {
    estimated-size = min-font-size
  }

  set text(size: estimated-size)

  // Extract header data
  let firstname = if "name" in data.header {
    let parts = data.header.name.split(" ")
    if parts.len() > 0 { parts.first() } else { "" }
  } else { "" }

  let lastname = if "name" in data.header {
    let parts = data.header.name.split(" ")
    if parts.len() > 1 { parts.slice(1).join(" ") } else { "" }
  } else { "" }

  let email = if "email" in data.header { data.header.email } else { "" }
  let phone = if "phone" in data.header { data.header.phone } else { "" }
  let github = if "github" in data.header {
    data.header.github.replace("github.com/", "")
  } else { "" }
  let linkedin = if "linkedin" in data.header {
    data.header.linkedin.replace("linkedin.com/in/", "")
  } else { "" }
  let homepage = if "website" in data.header {
    "https://" + data.header.website
  } else { "" }
  let location = if "location" in data.header { data.header.location } else { "" }

  // Determine position titles from summary or most recent role
  let positions = ()
  if "summary" in data and data.summary != none and data.summary != "" {
    positions = (data.summary,)
  } else if "experience" in data and data.experience.len() > 0 {
    positions = (data.experience.first().role,)
  }

  // Set up resume
  show: resume.with(
    author: (
      firstname: firstname,
      lastname: lastname,
      email: email,
      phone: phone,
      github: github,
      linkedin: linkedin,
      homepage: homepage,
      address: location,
      positions: positions,
    ),
    date: "",
    language: "en",
    colored-headers: true,
    show-footer: false,
    paper-size: "us-letter",
    accent-color: accent-color,
    profile-picture: none,
  )

  // Education section
  if "education" in data and data.education.len() > 0 {
    [= Education]

    for edu in data.education {
      let date-str = if "start_date" in edu and "end_date" in edu {
        let start = edu.start_date
        let end = edu.end_date
        start + " - " + end
      } else { "" }

      resume-entry(
        title: edu.institution,
        location: if "location" in edu { edu.location } else { "" },
        date: date-str,
        description: edu.degree + (if "field" in edu { " in " + edu.field } else { "" }),
      )

      if "details" in edu and edu.details != none and edu.details.len() > 0 {
        resume-item[
          #for detail in edu.details {
            [- #detail]
          }
          #if "gpa" in edu and edu.gpa != none [
            - GPA: #edu.gpa
          ]
        ]
      }
    }
  }

  // Experience section
  if "experience" in data and data.experience.len() > 0 {
    [= Experience]

    for exp in data.experience {
      let date-str = if "start_date" in exp and "end_date" in exp {
        let start = exp.start_date
        let end = exp.end_date
        start + " - " + end
      } else { "" }

      resume-entry(
        title: exp.role,
        location: if "location" in exp { exp.location } else { "" },
        date: date-str,
        description: exp.company,
      )

      if "bullets" in exp and exp.bullets.len() > 0 {
        resume-item[
          #for bullet in exp.bullets {
            [- #bullet]
          }
        ]
      }
    }
  }

  // Projects section
  if "projects" in data and data.projects != none and data.projects.len() > 0 {
    [= Projects]

    for proj in data.projects {
      resume-entry(
        title: proj.name,
        location: if "subtitle" in proj { proj.subtitle } else { "" },
        date: if "dates" in proj { proj.dates } else { "" },
        description: "",
      )

      if "bullets" in proj and proj.bullets.len() > 0 {
        resume-item[
          #for bullet in proj.bullets {
            [- #bullet]
          }
        ]
      }
    }
  }

  // Skills section
  if "skills" in data {
    [= Skills]

    if "languages" in data.skills and data.skills.languages.len() > 0 {
      resume-skill-item(
        "Languages",
        data.skills.languages.map(s => s)
      )
    }

    if "frameworks" in data.skills and data.skills.frameworks.len() > 0 {
      resume-skill-item(
        "Frameworks",
        data.skills.frameworks.map(s => s)
      )
    }

    if "tools" in data.skills and data.skills.tools.len() > 0 {
      resume-skill-item(
        "Tools",
        data.skills.tools.map(s => s)
      )
    }

    if "concepts" in data.skills and data.skills.concepts.len() > 0 {
      resume-skill-item(
        "Concepts",
        data.skills.concepts.map(s => s)
      )
    }
  }
}
