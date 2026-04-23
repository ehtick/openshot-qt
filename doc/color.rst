.. Copyright (c) 2008-2026 OpenShot Studios, LLC
 (http://www.openshotstudios.com). This file is part of
 OpenShot Video Editor (http://www.openshot.org), an open-source project
 dedicated to delivering high quality video editing and animation solutions
 to the world.

.. OpenShot Video Editor is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

.. OpenShot Video Editor is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

.. You should have received a copy of the GNU General Public License
 along with OpenShot Library.  If not, see <http://www.gnu.org/licenses/>.

.. _color_ref:

Color
=====

Have you ever watched a movie and noticed that the shadows feel just a little blue and cool, while the sunny
outdoor shots glow with warm golden light? Or that a thriller looks gritty and desaturated while a romantic
comedy feels vibrant and soft? That is not a coincidence — it is the result of deliberate **color work**. Color
is one of the most powerful storytelling tools in video editing, and OpenShot gives you everything you need to
use it, even if you have never thought about color before.

This guide is designed for everyone. We start from zero — what is color, how does a camera capture it,
and why does footage so often look flat or wrong right out of the camera? Then we build up naturally to the
professional tools inside OpenShot: scopes, color wheels, curves, and LUTs. By the end you will be able to
fix problem footage *and* give your videos a beautiful, intentional look.

.. image:: images/color-grade-view.jpg

*The OpenShot Color View: video preview in the center, Color Wheels dock on the right, and video scopes
(Luma Waveform and Histogram) below.*

.. _color_basics_ref:

Understanding Color
-------------------

Before touching any sliders, it helps to understand what color actually is in a digital video file.

How Red, Green, and Blue Make Every Color
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Your camera sensor, your monitor, and OpenShot's rendering engine all work the same way: every pixel is made
of exactly three numbers — a **Red** value, a **Green** value, and a **Blue** value. Each value typically
ranges from 0 (none of that color) to 255 (the maximum amount).

Here is the essential vocabulary:

- **Pure red** is R=255, G=0, B=0.
- **Pure green** is R=0, G=255, B=0.
- **Pure blue** is R=0, G=0, B=255.
- **White** is R=255, G=255, B=255 — all three channels at maximum.
- **Black** is R=0, G=0, B=0 — all three channels at zero.
- **Gray** is any value where R, G, and B are equal — for example R=128, G=128, B=128.

When you combine any two primary colors:

- Red + Green = **Yellow**
- Red + Blue = **Magenta** (pink-purple)
- Green + Blue = **Cyan** (blue-green)

This is called **additive color mixing**, and it is why your TV screen looks white when all the tiny red,
green, and blue sub-pixels are lit up at full brightness.

What Does "Exposure" Mean?
^^^^^^^^^^^^^^^^^^^^^^^^^^

Exposure is simply how bright or dark an image is. In camera terms, more light hitting the sensor means higher
R, G, and B values across the frame. An *overexposed* shot has many pixels near 255 — so bright that detail is
lost. An *underexposed* shot has many pixels near 0 — so dark that you cannot make out what is happening in
the shadows.

What Is Contrast?
^^^^^^^^^^^^^^^^^

Contrast is the difference between the brightest and darkest parts of your image. High contrast means bright
areas are very bright and dark areas are very dark, creating drama. Low contrast means the image looks "flat"
or "milky." Film and cameras tend to capture footage with more contrast than life itself — or sometimes less,
depending on the camera profile used.

What Is Saturation?
^^^^^^^^^^^^^^^^^^^

Saturation describes how *colorful* an image is. A fully saturated red is vivid and bold. A desaturated red
is dull and grayish. Zero saturation removes all color entirely, giving you a black-and-white image. Most
cameras record footage with a little less saturation than reality so editors have room to adjust.

What Is Hue?
^^^^^^^^^^^^

Hue is what we normally call "color" in everyday language — red, yellow, green, teal, blue, purple. Adjusting
hue shifts all the colors around a circular color wheel. This is less commonly used for correction but can
create interesting stylistic effects.

.. _white_balance_ref:

White Balance — Making Whites Look White
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Here is a situation almost every new video editor runs into: you film indoors under warm light bulbs, and when
you play it back, everything looks orange. Or you film in open shade and the footage looks cold and blue. That
is a **white balance** problem.

Different light sources emit different colors of light:

- **Candles and incandescent bulbs** are very warm (orange-yellow).
- **Fluorescent office lights** are often greenish.
- **Overcast daylight** is cool and slightly blue.
- **Direct noon sunlight** is roughly neutral.

Your camera tries to automatically detect what kind of light is present and correct for it, so that a white
piece of paper looks white. This is called **auto white balance**. It usually does a reasonable job, but it
can guess wrong — especially when the light changes mid-scene or the frame contains lots of one color.

When white balance is off, your first task in color correction is to neutralize it so that neutrals (white,
gray, skin) actually look neutral. In OpenShot, you do this with the **Temperature** and **Tint** controls of
the :guilabel:`Color Grade` effect:

- **Temperature** shifts the image warmer (more yellow-orange) or cooler (more blue). If your footage looks
  too orange, slide Temperature toward negative (cooler).
- **Tint** shifts the image toward green or magenta. It is used for fine-tuning after Temperature — for
  example, correcting the green tinge that fluorescent lights add.

A quick way to check white balance is to look at something in your shot that should be neutral — a white
wall, a gray t-shirt, or the whites of someone's eyes. If those look neutral on a calibrated monitor, your
white balance is probably correct.

.. _skin_tones_ref:

Skin Tones
^^^^^^^^^^

Human faces are the most scrutinized subjects in video. Viewers instinctively sense when skin tones look
wrong, even if they cannot say why. Good skin tones are warm (they lean orange, not green or blue) and retain
texture in the highlights.

A useful rule of thumb: **in a correctly balanced and graded image, all human skin tones — regardless of
race — fall roughly along the same diagonal line on a vectorscope** (a color-analysis tool). They shift
lighter or darker and more or less saturated, but they generally fall in the orange-to-yellow-orange zone of
the color wheel.

To evaluate and correct skin tones in OpenShot:

1. Add the :guilabel:`Color Grade` effect to your clip.
2. Open the :guilabel:`Color Wheels` dock.
3. Use the **Global** wheel to nudge the overall image toward warm orange if skin looks too cool.
4. If skin looks washed out, slightly lift **Midtones** saturation or use the **Curve: Red** to brighten
   the reds slightly in the mid range.
5. Avoid turning Saturation up too high — over-saturated skin looks unnatural.

.. _color_correction_ref:

Color Correction
----------------

**Color correction** is the process of fixing problems in your footage — making it look the way reality
actually appeared, or at least the way a typical viewer would expect. Think of it as restoring the image to a
neutral, clean starting point.

The most common things you will be correcting are:

- Incorrect white balance (footage is too warm or too cool).
- Wrong exposure (footage is too bright or too dark).
- Flat contrast (footage looks dull and milky).
- Washed-out or dull colors (saturation issues).

The goal of color correction is a solid, neutral foundation. Color grading (see :ref:`color_grading_ref`) then
uses that foundation to build your creative look on top.

Setting Up the Color Grade Effect
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :guilabel:`Color Grade` effect is the heart of OpenShot's color workflow. It combines correction,
curves, wheels, and LUT support in a single, animated effect.

To add it to a clip:

1. Right-click the clip on the timeline.
2. Choose :guilabel:`Color` from the context menu, then select a quick preset like
   :guilabel:`Auto Contrast`, :guilabel:`Lift Shadows`, :guilabel:`Warm Up`, or :guilabel:`Boost Color`.
   OpenShot will add a :guilabel:`Color Grade` effect automatically.
3. Or drag the **Color Grade** effect from the :guilabel:`Effects` tab onto your clip manually.
4. With the clip selected, right-click the Color Grade effect icon and choose :guilabel:`Properties` to open
   the property editor.

For a full-screen color workspace, go to :guilabel:`View → Views → Color View`. This rearranges the
interface to show a larger video preview, the :guilabel:`Color Wheels` dock on the right, and the
:guilabel:`Luma Waveform` and :guilabel:`Histogram` scopes below.

Primary Correction Controls
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

These controls live in the :guilabel:`Properties` panel when the Color Grade effect is selected. They are your
main tools for correction:

.. table::
   :widths: 20 80

   ========================  =============================================================
   Property                  What It Does
   ========================  =============================================================
   Temperature               Warms (positive) or cools (negative) the entire image. Use
                             this to fix white balance first.
   Tint                      Fine-tunes green/magenta balance. Positive adds magenta,
                             negative adds green. Use this after Temperature to finish
                             white balance.
   Exposure                  Makes the whole image brighter (positive) or darker
                             (negative). Use this to fix overall brightness.
   Contrast                  Expands the difference between lights and darks (positive)
                             or compresses it (negative). Positive contrast gives a
                             punchier image; negative gives a flat, low-contrast look.
   Highlights                Brightens or darkens only the bright parts of the image.
                             Negative values "recover" overexposed highlights.
   Shadows                   Lifts or lowers only the dark parts. Positive values "open
                             up" dark shadows so you can see detail there.
   Saturation                Controls overall color intensity. 1.0 is unchanged, 0.0 is
                             grayscale, 2.0 doubles the color.
   Vibrance                  Like Saturation, but smarter — it preferentially boosts
                             colors that are already muted, without oversaturating colors
                             that are already vivid. Great for a natural-looking boost.
   ========================  =============================================================

A Correction Workflow
^^^^^^^^^^^^^^^^^^^^^^

Work in this order for the best results:

1. **Fix white balance first** — use Temperature and Tint until neutrals look neutral.
2. **Set exposure** — use Exposure until the image brightness feels correct.
3. **Adjust contrast** — expand or compress the tonal range to taste.
4. **Recover highlights and shadows** — if bright areas are blown out or dark areas are crushed,
   use Highlights and Shadows to pull them back.
5. **Adjust saturation** — increase Saturation or Vibrance if colors look dull, or decrease if they
   look garish.

Once you are happy with the overall correction, you can move on to the scopes, wheels, and curves for
more precise work.

.. _color_scopes_ref:

Video Scopes — Analyzing Your Image Accurately
----------------------------------------------

Your monitor is not reliable for color work unless it has been professionally calibrated, and even then
the room lighting affects what you see. **Video scopes** are precision measurement tools that show you
the actual pixel values in your image as numbers and graphs. They never lie, even if your monitor does.

OpenShot includes two scopes: the **Luma Waveform** and the **Histogram**. Both update live as the
playhead moves. You can open both from :guilabel:`View → Docks → Luma Waveform` and
:guilabel:`View → Docks → Histogram`, or switch to the Color View to see them automatically.

.. _luma_waveform_ref:

The Luma Waveform
^^^^^^^^^^^^^^^^^^

The Luma Waveform is the most useful scope for exposure and tonal balance. It is a graph where:

- **The horizontal axis** represents the horizontal position across your video frame (left side of the
  graph = left side of the image, right side = right side of the image).
- **The vertical axis** represents brightness, from 0% (pure black) at the bottom to 100% (pure white,
  also called 100 IRE) at the top.

Every pixel in your image is plotted as a dot on this graph. Where many pixels share the same brightness at
the same horizontal position, the dot glows brighter. Where fewer pixels exist, the dot is dim.

**How to read it:**

- If most of the waveform clusters near the **bottom**, your image is too dark (underexposed).
- If most of the waveform is crammed against the **top**, your image is overexposed.
- A well-exposed image typically has the brightest elements between 70–90 IRE (the horizontal dashed line
  at 90%) and the darkest shadows above 0–5 IRE.
- A **flat, midrange cluster** (all content between 30–70%) means low contrast — the image will look milky.

IRE reference lines at 10%, 50%, and 90% appear as faint dashed lines to guide your eye.

Waveform Modes
^^^^^^^^^^^^^^

OpenShot's Luma Waveform dock has a dropdown to switch modes. Each mode shows different information:

.. table::
   :widths: 20 80

   ===================  ====================================================================
   Mode                 What It Shows
   ===================  ====================================================================
   Luma                 Brightness only (ignores color). The most useful mode for exposure
                        and contrast work. Shows where the highlights, midtones, and shadows
                        in your image actually live. Color of the trace can be changed to
                        Green, White, or Orange using the second dropdown.
   RGB Overlay          All three color channels (red, green, blue) drawn on top of each
                        other with their natural colors. Where channels overlap you see a
                        mixed color. Useful for quickly checking channel balance.
   RGB Parade           Splits the display into three side-by-side panels: red, green, and
                        blue. The height of each panel works exactly like the Luma waveform
                        but for that single channel. If one panel is noticeably higher than
                        the others in areas that should be neutral (gray or white), your
                        white balance is off. For example, if the blue panel sits higher than
                        red and green in the highlights, your image is too cool (blue).
   Red                  Shows only the red channel, displayed in red.
   Green                Shows only the green channel, displayed in green.
   Blue                 Shows only the blue channel, displayed in blue.
   ===================  ====================================================================

**RGB Parade is especially useful for white balance.** A perfectly neutral white or gray in your image will
show up at the same height in all three panels. If blue is higher than red, add warmth (positive Temperature).
If green is higher than both, add negative Tint.

Crushing Blacks
^^^^^^^^^^^^^^^^

"Crushing blacks" means pushing the darkest parts of your image all the way to 0 IRE — true black with no
detail. This is a stylistic choice (common in cinematic and thriller looks) but can also happen accidentally
if you push Contrast too high.

On the Luma Waveform, crushed blacks appear as a thick horizontal line packed against the very bottom of the
graph. If you want clean shadows with retained detail, keep the bottom of the waveform slightly above 0
(around 3–5%). If you *want* a crushed-black look, slide Shadows down until the waveform touches bottom.

To lift crushed blacks and reveal shadow detail:

- Raise the **Shadows** control in the Color Grade effect.
- Or use the **Curve: All** editor and add a point near the bottom-left, pulling it slightly upward.

.. _histogram_ref:

The Histogram
^^^^^^^^^^^^^

The Histogram is a different kind of graph. Instead of plotting pixels by their horizontal position in the
frame, it sorts all pixels by their brightness value (0 to 255) and shows you how many pixels exist at each
brightness level — as a bar chart.

- **The horizontal axis** goes from pure black (left) to pure white (right).
- **The vertical axis** shows how many pixels in your image have that brightness value. Taller bars = more
  pixels at that brightness.
- The graph shows four overlapping colors: red, green, and blue channels plus luma (white/gray).

**How to read it:**

- If bars are **clustered at the left**, the image is dark (underexposed).
- If bars are **clustered at the right** or press against the right edge, the image is bright (overexposed).
  A sharp cutoff against the right wall usually means highlight clipping — detail has been lost.
- A **well-exposed image** typically has bars spread across the middle of the histogram, with highlights that
  taper off before reaching the far right edge.
- A **low-contrast image** has bars bunched into a narrow hill in the middle, not reaching either edge.
  Increasing Contrast will spread them out.

Histogram Channels and Scale
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Histogram dock has two dropdowns:

**Channel selector:**

- **All Channels** — Shows red, green, blue, and luma all overlaid. This is the most informative starting
  view because you can see if any single channel is clipping or shifted.
- **Luma** — Shows only the overall brightness distribution. Use this for exposure decisions.
- **Red / Green / Blue** — Shows a single channel's distribution. Useful when diagnosing color casts.
  For example, if the Red histogram extends further right than Green and Blue, the image is warm.

**Scale selector:**

- **Logarithmic** — Compresses high counts so even rarely-used tonal values are visible. Most useful for
  general color work because you can see if any regions of the tonal range are completely empty.
- **Linear** — Shows raw counts. The highest bars can dwarf everything else. Useful when you need to see the
  exact relative weight of each tone.

.. _color_grading_ref:

Color Grading
--------------

If color correction is about making your footage look *right*, then **color grading** is about making it look
*intentional*. Grading is where you build the visual mood, emotion, and style of your video.

A grade is a creative choice:

- Do you want a warm, golden nostalgic feel?
- A cold, clinical, desaturated look?
- Teal shadows and orange highlights — the signature "blockbuster" look?
- A faded, lifted-black "film" aesthetic?

The tools for grading are the same ones you use for correction, just pushed further with intention. OpenShot's
:guilabel:`Color Wheels`, :guilabel:`Curve Editor`, and :guilabel:`LUT files` are the primary grading tools.

.. _color_wheels_ref:

Color Wheels
^^^^^^^^^^^^^

Color wheels let you push color into specific **tonal ranges** — shadows, midtones, and highlights — without
affecting the others. This is the tool professional colorists use most.

.. image:: images/color-wheel-overall.jpg

*The Color Wheels dock, showing Global, Shadows, Midtones, and Highlights wheels.*

OpenShot has four wheels in the :guilabel:`Color Wheels` dock:

.. table::
   :widths: 20 80

   ===================  ========================================================================
   Wheel                What It Affects
   ===================  ========================================================================
   Global               Applies a color tint to the **entire image** at all brightness levels.
                        Use this for an overall hue push — for example, a gentle warm shift
                        everywhere.
   Shadows              Applies color only to the **darkest parts** of the image. Great for
                        adding a cool blue or teal tint to shadows — a classic cinematic move.
   Midtones             Applies color to the **middle tones** — the most common skin tone and
                        background regions. The most sensitive wheel, because the eye notices
                        midtone shifts quickly.
   Highlights           Applies color only to the **brightest parts** of the image. Warming
                        highlights (pushing them toward orange or yellow) while keeping shadows
                        cool is the foundation of the teal-and-orange look.
   ===================  ========================================================================

**How to use a color wheel:**

- Click and drag the **central dot** to push color in that direction. Dragging toward red adds red; dragging
  toward the opposite edge (cyan) removes red.
- The further from the center you drag, the stronger the effect.
- The **Amount** slider below each wheel adjusts overall intensity. Lower it to blend the tinted result
  back toward the unaffected image.
- The **Luma** slider adjusts the brightness of that tonal zone. Positive values brighten shadows or
  highlights; negative values darken them.
- Right-click any wheel in the Properties panel to access **Reset**, which returns that wheel to neutral.

**Opening the Color Wheels dock:**

Click the :guilabel:`Color Wheels` row in the Properties panel when a Color Grade effect is selected, or
switch to :guilabel:`View → Views → Color View`.

The Classic Teal-and-Orange Look
""""""""""""""""""""""""""""""""""

This is the most popular cinematic grade in modern film. Here is how to build it:

1. Open the Color Wheels dock.
2. Drag the **Shadows** wheel toward teal (blue-green, upper-left area of the wheel).
3. Drag the **Highlights** wheel toward orange (lower-right).
4. Optionally drag **Midtones** very slightly toward orange to warm skin.
5. Reduce Amount on both Shadows and Highlights to about 0.3–0.5 so the effect is not overdone.

.. _curves_ref:

Curves — Precise Tonal and Color Control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Curves are the most powerful and flexible color tool available. A curve is a graph where:

- **The horizontal axis** represents the input value (how bright or colorful the pixel is before your
  adjustment).
- **The vertical axis** represents the output value (what it becomes after the adjustment).

When the curve is a perfectly straight diagonal line (bottom-left to top-right), the image is unchanged.
When you bend the curve, you are changing the relationship between input and output.

.. image:: images/color-curve-editor.jpg

*The OpenShot Curve Editor. Add points by clicking, drag them to reshape the curve, right-click to change
interpolation.*

**Adding and editing points:**

1. Open the Curve Editor by clicking any **Curve** row in the Properties panel (Curve: All, Curve: Red,
   Curve: Green, or Curve: Blue) or by double-clicking the curve thumbnail.
2. Click anywhere on the diagonal line to add a new control point.
3. Drag the point to reshape the curve. Moving a point up makes those tones brighter; moving it down makes
   them darker.
4. Right-click a point to change its **interpolation** (Bezier, Linear, or Constant) or to remove it.
5. Press :kbd:`Delete` or :kbd:`Backspace` on a selected point to remove it.
6. The curve editor uses keyframes — changes at the current playhead position create keyframe values, so
   you can animate the curve over time.

Common Curve Shapes
""""""""""""""""""""

**S-curve (add contrast):**
The most common correction. Add a point in the upper quarter and pull it slightly up (brightens highlights),
and add a point in the lower quarter and pull it slightly down (darkens shadows). The image gains contrast and
"pop" without affecting the mid-gray point.

**Lift (raise blacks):**
Drag the very bottom-left corner of the curve (where the line meets the left wall at black) upward. This
raises the black point — shadows never go fully to black. This is the foundation of the faded-film aesthetic.

**Lower highlights:**
Add a point in the upper-right and drag it downward. Brings overexposed or very bright areas down without
affecting the rest of the image.

**The Four Curve Channels:**

- **Curve: All** — Affects overall brightness across all channels simultaneously. Most commonly used.
- **Curve: Red** — Adjusts only the red channel. Pulling it up adds red (warms the image), pulling it down
  removes red (adds cyan). Great for tonal color grading — for example, add a point in the shadows and pull
  it slightly down to add cyan tint to shadows.
- **Curve: Green** — Adjusts the green channel. Pulling up adds green; pulling down adds magenta.
- **Curve: Blue** — Adjusts the blue channel. Pulling up adds blue (cools); pulling down adds yellow/orange
  (warms). Common grading move: pull the Blue Shadows point slightly up (cool teal shadows) and pull the Blue
  Highlights point slightly down (warm orange highlights).

Why use curves instead of simple sliders?
""""""""""""""""""""""""""""""""""""""""""

Sliders like Temperature and Saturation affect the *whole* image uniformly. Curves let you apply different
adjustments to different brightness levels in the same operation. For example, you can warm the highlights
while simultaneously cooling the shadows — all in one curve — without separate settings for each tonal zone.
This makes curves the most precise and efficient tool for advanced color work.

.. _lut_ref:

LUT Files — One-Click Color Looks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A **LUT** (Lookup Table, pronounced "lut") is a pre-made color transformation stored in a small file.
Think of it as a color recipe: the LUT says "for every pixel with *this* color, output *that* color instead."

LUTs are created by professional colorists and can recreate the look of specific film stocks, cameras, or
cinematic styles with a single click. OpenShot supports LUT files in the industry-standard **.cube** format.

OpenShot ships with a built-in collection of LUTs across five style categories — see the :ref:`effects_ref`
page for a visual gallery of all included looks.

You can also download free **.cube** LUT packs from many online resources and photography communities.

**How to apply a LUT in OpenShot:**

1. Select your clip and open the :guilabel:`Color Grade` effect properties.
2. Click the :guilabel:`LUT File` property and browse to your **.cube** file.
3. The LUT is applied immediately. Use the :guilabel:`LUT Intensity` slider (0.0–1.0) to blend between the
   original image and the fully transformed look.

Blending LUTs
"""""""""""""

The :guilabel:`LUT Intensity` slider is powerful. At 1.0, the full LUT transformation is applied.
At 0.5, you get a 50/50 blend between your corrected image and the LUT look. At 0.0, the LUT has no effect.

This lets you dial in exactly *how much* of a look you want, rather than being stuck at full intensity.
Typically, professional colorists apply LUTs at 0.4–0.7 rather than 1.0 for a more natural, integrated feel.

You can also **stack** a Color Grade effect with separate Color Map / Lookup effects to layer multiple LUTs,
blending each one individually.

LUT Best Practices
""""""""""""""""""

- **Correct before you grade.** Apply your LUT *after* doing primary correction (white balance, exposure,
  contrast). LUTs are designed to work on properly balanced footage. A LUT applied to footage with a strong
  color cast will look wrong.
- **Most included LUTs are designed for Rec. 709 footage** — the standard for HD video cameras and
  smartphones. If your camera records in a LOG profile (a flat, desaturated profile designed for more
  latitude in post), you may need a different LUT designed for that specific LOG format first.
- **Try multiple looks.** Because LUT Intensity lets you blend, you can try bold looks and back them off.
  Do not be afraid to experiment.

.. _color_mix_ref:

The Mix Control — Blending Your Grade Into the Original
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

At the bottom of the Color Grade effect properties is the **Mix** control (range 0.0–1.0).

- At **1.0** (the default), the fully graded image is shown — all of your corrections, wheels, curves,
  and LUT are fully applied.
- At **0.0**, the original ungraded image is shown — as if you had no Color Grade effect at all.
- At **0.5**, you see a 50/50 blend of the original and graded image.

This is useful when your grade is overall correct but feels slightly overdone. Instead of tweaking every
individual control, you can simply dial Mix back to 0.8 or 0.7 to soften the entire grade at once.

Mix is also keyframable — you can animate the grade fading in or out over time, for example having a scene
start in a desaturated, flat look and gradually bloom into full color.

.. _color_workflow_ref:

Putting It All Together — A Complete Workflow
----------------------------------------------

Here is a step-by-step tutorial for grading a clip from start to finish.

Step 1 — Prepare Your Workspace
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Go to :guilabel:`View → Views → Color View` to switch to the color grading layout.
2. Select the clip you want to grade on the timeline.
3. Right-click the clip and choose :guilabel:`Color → Auto Contrast` to add a Color Grade effect with a
   useful starting point.

Step 2 — Check the Scopes First
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Before touching any controls, look at the **Luma Waveform** and **Histogram**:

- Is the image overall too bright or too dark? Check the waveform's vertical range.
- Is the image low contrast (flat)? The waveform will be in a narrow horizontal band.
- Is there a color cast? Switch the waveform to **RGB Parade** and check if all three channels are balanced.

These observations will tell you *what* to fix before you start adjusting.

Step 3 — Primary Correction
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

4. With the Color Grade effect properties open, set **Temperature** to fix white balance.
5. Set **Exposure** to correct overall brightness.
6. Set **Contrast** to give the image tonal punch.
7. Use **Highlights** and **Shadows** to recover any blown-out or crushed areas.
8. Gently adjust **Saturation** or **Vibrance**.
9. Keep checking the scopes as you work — aim for a waveform that has shadows above 5%, highlights below 95%,
   and a spread across the full tonal range.

Step 4 — Color Wheels for Tonal Color Separation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

10. Open the :guilabel:`Color Wheels` dock.
11. Decide on your grade's emotional direction — warm and golden? Cool and moody? Teal and orange?
12. Gently push the **Shadows** wheel toward your desired shadow color.
13. Gently push the **Highlights** wheel toward your desired highlight color.
14. Adjust the **Amount** sliders to control intensity.
15. Use **Midtones** carefully — this affects skin tones most strongly.

Step 5 — Fine-Tune with Curves
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

16. Open **Curve: All** and add a gentle S-curve for contrast if the image still feels flat.
17. Open **Curve: Blue** and pull the lower-left point slightly up (cools shadows) and the upper-right
    slightly down (warms highlights) for a cinematic feel.
18. Open **Curve: Red** if skin tones need warming — a slight lift in the mid-range.

Step 6 — Apply a LUT (Optional)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

19. Browse to a **.cube** LUT file in the **LUT File** property.
20. Set **LUT Intensity** to 0.5 and evaluate — then dial it up or down.

Step 7 — Final Blend
^^^^^^^^^^^^^^^^^^^^^

21. If the overall grade feels too heavy, lower the **Mix** control to 0.7–0.9 to blend in some of the
    original image.
22. Compare: toggle the Color Grade effect on and off by right-clicking it and choosing
    :guilabel:`Toggle Effect` to see a before/after.

Step 8 — Apply to Other Clips
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

23. Once you are happy with the grade on one clip, you can apply the same look to other clips:
    right-click the Color Grade effect icon and use :guilabel:`Copy`, then select another clip and
    :guilabel:`Paste Effects`.
24. Or use the :guilabel:`Parent` property to link multiple clips' Color Grade effects to a single
    parent effect — change the parent and all children update at once. See :ref:`effect_parent_ref`.

For more information on animating color properties over time, see :ref:`animation_ref`.
For a complete list of all Color Grade properties, see :ref:`effects_ref`.
