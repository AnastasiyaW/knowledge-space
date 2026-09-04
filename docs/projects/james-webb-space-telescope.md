---
title: James Webb Space Telescope — First Images Release
category: projects
tags: [first-images-release, james-webb-space-telescope, james_webb_space_telescope, project]
aliases: ["James Webb Space Telescope"]
---

# James Webb Space Telescope — First Images Release

**Development line:** `project:james-webb-space-telescope` · thread `first-images-release`  
**Events:** 1 dated, 2022-07-12 → 2022-07-12 · **Researched:** 2026-09-04 · confidence: medium

## What it is

James Webb Space Telescope is an active NASA, ESA, and CSA infrared observatory for astronomers analysing public space-observatory data.

- MAST provides raw, calibrated, and high-level products.
- The open-source JWST pipeline processes every instrument and observing mode with CRDS reference files.

## Development line

- **2022-07-12 — James Webb Space Telescope first public images released.** Webb transitioned from commissioning to public science delivery on 2022-07-12. The release gave the public and scientific community their first broad view of the telescope's observational capability.

## What changed

- **2022-07-12.** The SMACS 0723 Hubble/Webb comparison turned the first deep field into a direct capability test. This was a public-science milestone, not a hardware change.
- **2022-07-13.** A media asset added the WASP-96 b NIRISS transmission spectrum, expanding the initial release from pictures to exoplanet spectroscopy. The source asset appeared on 2022-07-12, so 2022-07-13 marks distribution rather than a new observing mode.
- **2026-09-04.** Webb remains active. MAST reprocesses data products after each quarterly operations build, so earlier downloads are not necessarily current calibrated products.

## How to use this

From 2022-07-12, treat JWST first-image releases as the historical boundary between commissioning and public scientific-observation delivery when describing the project’s operational maturity.

1. Check whether the required observations are public. Retrieve public MAST data anonymously, or authenticate with MyST credentials and programme authorization for exclusive-access data.
  — <https://jwst-docs.stsci.edu/accessing-jwst-data>
2. Search MAST Portal by programme, instrument, mode, coordinates, or target. Use JWST Mission Search for JWST-specific filters.
  — <https://jwst-docs.stsci.edu/accessing-jwst-data/mast-web-access>
3. Download minimum recommended products first. Select raw, intermediate, guide-star, or reference files only when the analysis needs them.
  — <https://jwst-docs.stsci.edu/accessing-jwst-data/mast-web-access>
4. For reprocessing, install a released jwst pipeline on Linux or macOS. Configure CRDS before importing the package, then run the stages appropriate to the observing mode.
  — <https://jwst-docs.stsci.edu/jwst-science-calibration-pipeline>
5. For a publication, record the pipeline version and CRDS context, cite the data, and include the required mission acknowledgement.
  — <https://jwst-docs.stsci.edu/accessing-jwst-data/citing-jwst-data>

## Best practices

- Start with MAST's minimum recommended products rather than downloading raw data by default. Retrieve lower-level products only for a defined reduction need.
  — <https://jwst-docs.stsci.edu/accessing-jwst-data/mast-web-access>
- Use the Operations pipeline build and its compatible default CRDS context for general analysis. Development builds are not the default recommendation.
  — <https://jwst-docs.stsci.edu/jwst-science-calibration-pipeline>
- Record both the jwst software version and CRDS context whenever results depend on reprocessing or a context override.
  — <https://jwst-docs.stsci.edu/accessing-jwst-data/citing-jwst-data>
- Check current calibration status and known issues before interpreting a downloaded product as final, because archive products and calibration versions change quarterly.
  — <https://jwst-docs.stsci.edu/accessing-jwst-data>

## Superseded by this

- The 2022-07-12 first-image comparison as an analysis baseline is superseded by the current MAST archive release, because products are reprocessed after each quarterly operations build.
- The pre-October 2024 practice of pairing released jwst software with a moving CRDS context is obsolete. Each pipeline version now selects a compatible frozen default context, and overrides must be documented.

## Still unknown

- The ImgSli page did not render during research, leaving its exact caption, source-image versions, and processing settings unverified.
- The WASP-96 b asset itself is dated 2022-07-12; the 2022-07-13 event date therefore cannot establish a separate instrument or mission change.
- The two dated records concern one telescope but two different first-image outputs: a SMACS 0723 imaging comparison and a WASP-96 b transmission spectrum.

## Sources

| source | title | read |
|---|---|---|
| https://imgsli.com/MTE2Mjc3 | ImgSli item MTE2Mjc3 — Hubble/JWST comparison of SMACS 0723; page did not render during research | 2026-09-04 |
| https://webbtelescope.org/contents/media/images/2022/032/01G72VSFW756JW5SXWV1HYMQK4?Collection=First+Images&news=true | Exoplanet WASP-96 b (NIRISS Transmission Spectrum) | 2026-09-04 |
| https://commons.wikimedia.org/wiki/File%3AExoplanet_WASP-96_b_%28NIRISS_Transmission_Spectrum%29_%282022-032-01G72VSFW756JW5SXWV1HYMQK4%29.png | File: Exoplanet WASP-96 b (NIRISS Transmission Spectrum) | 2026-09-04 |
| https://science.nasa.gov/mission/webb/webb-mission-timeline/ | Webb Mission Timeline | 2026-09-04 |
| https://science.nasa.gov/missions/webb/nasas-webb-delivers-deepest-infrared-image-of-universe-yet/ | NASA’s Webb Delivers Deepest Infrared Image of Universe Yet | 2026-09-04 |
| https://science.nasa.gov/mission/webb/ | James Webb Space Telescope | 2026-09-04 |
| https://jwst-docs.stsci.edu/accessing-jwst-data | Accessing JWST Data | 2026-09-04 |
| https://jwst-docs.stsci.edu/accessing-jwst-data/mast-web-access | MAST Web Access | 2026-09-04 |
| https://jwst-docs.stsci.edu/jwst-science-calibration-pipeline | JWST Science Calibration Pipeline | 2026-09-04 |
| https://jwst-docs.stsci.edu/accessing-jwst-data/citing-jwst-data | Citing JWST Data | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:james-webb-space-telescope`, thread `first-images-release`, 1 dated events 2022-07-12 → 2022-07-12.
- **Practical note:** From 2022-07-12, treat JWST first-image releases as the historical boundary between commissioning and public scientific-observation delivery when describing the project’s operational maturity.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
