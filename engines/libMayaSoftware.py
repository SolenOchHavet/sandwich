#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Engine "Maya Software"

This adds support for Maya Software

"""


class Engine(object):
    def __init__(self, iMayaVersion):
        self.iMayaVersion = iMayaVersion
        self.sEngineName = "mayaSoftware"
        self.sDisplayName = "Maya Software"
        self.lstNodes = (("defaultRenderQuality", "$RQ"), 
            ("defaultRenderGlobals", "$RG"))
        self.bIsInstalled = False

        self.setup()

    def attributes(self):
        """

        """

        return {
            # Contains:
            # ss (shadingSamples), mss (maxShadingSamples), mvs (visibilitySamples), mvm (maxVisibilitySamples)
            # pss (particleSamples)
            0: "$RQ.ss:$RQ.mss:$RQ.mvs:$RQ.mvm:$RQ.pss",

            # Contains:
            # ufil (useMultiPixelFilter), pft (pixelFilterType), pfwx (pixelFilterWidthX), pfwy (pixelFilterWidthY)
            1: "$RQ.ufil:$RQ.pft:$RQ.pfwx:$RQ.pfwy",

            # Contains:
            # rct (redThreshold), gct (greenThreshold), bct (blueThreshold), cct (coverageThreshold)
            2: "$RQ.rct:$RQ.gct:$RQ.bct:$RQ.cct",

            # Contains:
            # ert (enableRaytracing), rfl (reflections), rfr (refractions), sl (shadows), rtb (rayTraceBias)
            3: "$RQ.ert:$RQ.rfl:$RQ.rfr:$RQ.sl:$RQ.rtb",

            # Contains:
            # mb (motionBlur), mbt (motionBlurType), mbf (motionBlurByFrame), bll (blurLength), mbus (motionBlurUseShutter),
            # mbso (motionBlurShutterOpen), mbsc (motionBlurShutterClose), bls (blurSharpness), smc (smoothColor),
            # smv (smoothValue), kmv (keepMotionVector)
            4: "$RG.mb:$RG.mbt:$RG.mbf:$RG.bll:$RG.mbus:$RG.mbso:$RG.mbsc:" \
                "$RG.bls:$RG.smc:$RG.smv:$RG.kmv",

            # Contains:
            # fg (fogGeometry), afp (applyFogInPost), pfb (postFogBlur)
            5: "$RG.fg:$RG.afp:$RG.pfb",

            # Contains:
            # ifg (ignoreFilmGate)
            6: "$RG.ifg",

            # Contains:
            # TODO: "Shadow Linking" from Render Globals looks like two attributes that can have different configurations..
            # edm (enableDepthMaps)
            7: "$RG.edm",

            # Contains:
            # gama (gammaCorrection), clip (clipFinalShadedColor), jfc (jitterFinalColor), cth (compositeThreshold)
            8: "$RG.gama:$RG.clip:$RG.jfc:$RG.cth",

            # Contains:
            # uf (useFileCache), oi (optimizeInstances), rut (reuseTessellations), udbx (useDisplacementBoundingBox)
            9: "$RG.uf:$RG.oi:$RG.rut:$RG.udbx",

            # Contains:
            # rd (recursionDepth), lp (leafPrimitives), sp (subdivisionPower)
            10: "$RG.rd:$RG.lp:$RG.sp",

            # Contains:
            # npu (numCpusToUse)
            11: "$RG.npu",

            # Contains:
            # esr (enableStrokeRender), ope (oversamplePaintEffects), oppf (oversamplePfxPostFilter), ors (onlyRenderStrokes),
            # sdf (strokesDepthFile)
            12: "$RG.esr:$RG.ope:$RG.oppf:$RG.ors:$RG.sdf",
        }

    def displayName(self):
        """
        Returns the display name used in interfaces for the engine
        """

        return self.sDisplayName

    def engineName(self):
        """
        Returns the internal name for the engine name
        """

        return self.sEngineName

    def isInstalled(self):
        """
        Returns true if engine is installed and successfully loaded
        """

        return self.bIsInstalled

    def nodes(self):
        """
        Returns a list of all render settings nodes used for the engine
        """

        return self.lstNodes

    def renderCommand(self):
        """
        Returns the command necessary to execute a valid render using the 
        render engine. It needs to include the following options in this order:

        Maya path, start frame, end frame, width, height, camera, dir path,
        image name, path to Maya file
        """

        return "%s -r sw -s %s -e %s -pad 4 -fnc 3 -x %s -y %s -cam %s " \
            "-rd %s -im %s %s"

    def sections(self):
        """
        Returns all the sections of the render globals for the engine
        """

        return {
            0: "Anti-aliasing: Number of Samples",
            1: "Anti-aliasing: Multi-pixel Filtering",
            2: "Anti-aliasing: Contrast Threshold",
            3: "Raytracing Quality",
            4: "Motion Blur",
            5: "Render Options: Post Processing",
            6: "Render Options: Camera",
            7: "Render Options: Lights and Shadows",
            8: "Render Options: Color/Compositing",
            9: "Memory and Performance: Tessellation",
            10: "Memory and Performance: Ray Tracing",
            11: "Memory and Performance: Multi Processing",
            12: "Paint Effects Rendering Options",
        }

    def setup(self):
        """
        Makes sure the engine is loaded and that the render globals nodes 
        exists. This is executed on each startup of Sandwich but does only 
        takes time if the engine is loaded for the first time.
        """