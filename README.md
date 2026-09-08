# the.inner-circle.fyi

this is the git repo for the [the.inner-circle.fyi](https://the.inner-circle.fyi), the inner circle communities webring!.

## joining the webring

to inner circle members:

1. fork this repository
2. edit [`src/ticfyi/webring.py`](src/ticfyi/webring.py)'s `WEB_RING_MEMBERS` to include your domain.
3. upload your 88x31px button (if applicable) to [`src/ticfyi/public/images/member-buttons`](src/ticfyi/public/images/member-buttons) as a `.png`
4. create a pull request on this repository asking to be added to the webring
5. add the following html snippet to your website where you would like the webring to appear on your website

```html
<script src="https://the.inner-circle.fyi/ring/ring.js"></script>
```

> If the page is hosted on a different domain than the one you joined the webring with, you can specify the domain using the `data-domain` or `domain` attributes:
```html
<script src="https://the.inner-circle.fyi/ring/ring.js" data-domain="your.domain.com"></script>
```
> [!NOTE]
> This script places a new `div` with `id` `innerCircleWebRing` in the parent element of the script container. If you want to customise the location of the div, simply just add `<div id="innerCircleWebRing"></div>` to the page above wherever the script is loaded & it shall use that one instead.

6. done!
