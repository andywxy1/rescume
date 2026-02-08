// Rescume Template: Simple Technical Resume with Auto-Fit
// Based on simple-technical-resume package v0.1.1
// This template accepts structured data and auto-fits content to one page

#import "@preview/simple-technical-resume:0.1.1": *

// Auto-fit function: tries progressively smaller font sizes until content fits one page
#let auto-fit-resume(
  data,
  min-font-size: 9pt,
  default-font-size: 10.5pt,
  font-step: 0.5pt
) = {
  // Font sizes to try (from default down to minimum)
  let font-sizes = ()
  let current = default-font-size
  while current >= min-font-size {
    font-sizes.push(current)
    current = current - font-step
  }

  // For now, we'll use the default size and let the user iterate if needed
  // Full auto-fit requires Typst 0.12+ with measure() in context blocks
  // This is a simplified version that sets font size based on content length estimate

  let estimated-size = default-font-size

  // Rough heuristic: count total bullet points and content length
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

  // Adjust font size based on content volume
  if total-bullets > 20 {
    estimated-size = 9pt
  } else if total-bullets > 15 {
    estimated-size = 9.5pt
  } else if total-bullets > 12 {
    estimated-size = 10pt
  }

  // Ensure we don't go below minimum
  if estimated-size < min-font-size {
    estimated-size = min-font-size
  }

  // Set up the resume with calculated font size
  set text(size: estimated-size)

  // Extract header information
  let name = data.header.name
  let phone = if "phone" in data.header { data.header.phone } else { "" }
  let email = if "email" in data.header { data.header.email } else { "" }
  let linkedin = if "linkedin" in data.header { data.header.linkedin } else { "" }
  let github = if "github" in data.header { data.header.github } else { "" }
  let website = if "website" in data.header { data.header.website } else { "" }

  show: resume.with(
    top-margin: 0.4in,
    personal-info-font-size: estimated-size + 0.5pt,
    author-position: center,
    personal-info-position: center,
    author-name: name,
    phone: phone,
    email: email,
    website: website,
    linkedin-user-id: linkedin,
    github-username: github
  )

  // Summary section (optional)
  if "summary" in data and data.summary != none and data.summary != "" {
    block(
      above: 0.3em,
      below: 0.5em,
      text(size: estimated-size, style: "italic", data.summary)
    )
  }

  // Education section
  if "education" in data {
    custom-title("Education")[
      #for edu in data.education {
        education-heading(
          edu.institution,
          if "location" in edu { edu.location } else { "" },
          edu.degree,
          if "field" in edu { edu.field } else { "" },
          if "start_date" in edu { datetime(year: int(edu.start_date.split("-").at(0)), month: int(edu.start_date.split("-").at(1)), day: 1) } else { datetime.today() },
          if "end_date" in edu and edu.end_date != "Present" { datetime(year: int(edu.end_date.split("-").at(0)), month: int(edu.end_date.split("-").at(1)), day: 1) } else { "Present" }
        )[
          #if "details" in edu and edu.details != none {
            for detail in edu.details {
              [- #detail]
            }
          }
          #if "gpa" in edu and edu.gpa != none [
            - GPA: #edu.gpa
          ]
        ]
      }
    ]
  }

  // Experience section
  if "experience" in data {
    custom-title("Experience")[
      #for exp in data.experience {
        work-heading(
          exp.role,
          exp.company,
          if "location" in exp { exp.location } else { "" },
          if "start_date" in exp { datetime(year: int(exp.start_date.split("-").at(0)), month: int(exp.start_date.split("-").at(1)), day: 1) } else { datetime.today() },
          if "end_date" in exp { if exp.end_date == "Present" { "Present" } else { datetime(year: int(exp.end_date.split("-").at(0)), month: int(exp.end_date.split("-").at(1)), day: 1) } } else { "Present" }
        )[
          #if "bullets" in exp {
            for bullet in exp.bullets {
              [- #bullet]
            }
          }
        ]
      }
    ]
  }

  // Projects section
  if "projects" in data and data.projects != none and data.projects.len() > 0 {
    custom-title("Projects")[
      #for proj in data.projects {
        project-heading(
          proj.name,
        )[
          #if "bullets" in proj {
            for bullet in proj.bullets {
              [- #bullet]
            }
          }
        ]
      }
    ]
  }

  // Skills section
  if "skills" in data {
    custom-title("Skills")[
      #skills()[
        #if "languages" in data.skills and data.skills.languages.len() > 0 [
          - *Languages:* #data.skills.languages.join(", ")
        ]
        #if "frameworks" in data.skills and data.skills.frameworks.len() > 0 [
          - *Frameworks:* #data.skills.frameworks.join(", ")
        ]
        #if "tools" in data.skills and data.skills.tools.len() > 0 [
          - *Tools:* #data.skills.tools.join(", ")
        ]
        #if "concepts" in data.skills and data.skills.concepts.len() > 0 [
          - *Concepts:* #data.skills.concepts.join(", ")
        ]
      ]
    ]
  }
}
