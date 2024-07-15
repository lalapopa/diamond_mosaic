# Diamond painting pattern maker 

Convert your image to diamond painting pattern using one CLI command.
<p align="center">
  <img src="./source/main-image.svg" />
</p>


# Usage 

    python cli.py --help

    ╭─ options ──────────────────────────────────────────────────────────────────────────────────────╮
    │ -h, --help             show this help message and exit                                         │
    │ --image PATH           Path to `.png` or `.jpg` image. (required)                              │
    │ --d-num-w INT          How many diamonds (dots) will be along horizontal side. (default: 100)  │
    │ --d-num-h INT          How many diamonds (dots) will be along vertical side. You can skip this │
    │                        value if you defined `d_num_w`, using image pixel ratio this            │
    │                        value will be calculated. (default: 0)                                  │
    │ --save-name STR        Output files name. (default: result)                                    │
    │ --d-d FLOAT            Diamond diameter in centimeter. (default: 0.25)                         │
    ╰────────────────────────────────────────────────────────────────────────────────────────────────╯

Convert image to diamond painting scheme with 

    python cli.py --image YOUR_IMAGE.png

This will generate in current directory two files:

* `result.svg` actual pattern with 100 diamonds in width with labeled color in
  each cell
* `result.xlsx` MS Excel spreadsheet where:

|Amount in pieces|Color label|DMC color|Actual color| -  | -  | Color labels sorted in alphabetical order|DMC color|Color|
|---|---|---|---|---|---|---|---|---|
| 1 | FS| 739| !pale  | - | - |2F | 152 | !pinkish |
| ...  | ... | ... | ... | - | - | ... | ... | ... |

# todos

* [ ] Add way to pick different color palette and add your own (Some
  standardized file will be needed to implement that) 
* [ ] After about 700 cells in each side (half-mil cells) SVG rendering in
  browser or Inkscape will go BRR .
* [ ] Do More testing for now it's really dumb

