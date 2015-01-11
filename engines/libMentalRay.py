#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Engine "mental ray"

This adds support for mental ray

"""

import maya.cmds as mc
import maya.mel as mel


class Engine(object):
    def __init__(self, iMayaVersion):
        self.iMayaVersion = iMayaVersion
        self.sEngineName = "mentalRay"
        self.sDisplayName = "mental ray"
        self.lstNodes = (("mentalrayGlobals", "$MG"), 
            ("miDefaultOptions", "$DO"), ("miDefaultFramebuffer", "$DF"))
        self.bIsInstalled = False

    def attributes(self):
        """

        """

        return {
            # RENDERING FEATURES
            # renderMode, scanline, rayTracing, globalIllum, caustics, finalGather, motionBlur
            0: "$MG.rmo:$DO.scan:$DO.ray:$DO.gi:$DO.ca:$DO.fg:$DO.mb",

            # EXTRA FEATURES
            # faces, geometryShaders, lightMaps, lensShaders, displacementShaders, displacementPresample, volumeShaders,
            # volumeSamples, autoVolume, outputShaders, photonAutoVolume, mergeSurfaces, renderHair
            1: "$DO.fac:$DO.geo:$DO.lim:$DO.lens:$DO.dis:$DO.dipr:$DO.vol:" \
                "$DO.vos:$DO.avo:$DO.out:$DO.phav:$DO.mrg:$DO.rha",

            # CONTOURS
            # contourEnable, contourClearImage, contourClearColor, contourSamples, contourFilter, contourFilterSupport
            2: "$DF.ce:$DF.cci:$DF.ccc:$DF.cs:$DF.cf:$DF.cfs",

            # CONTOURS: DRAW BY PROPERTY DIFFERENCE
            # contourBackground, contourPriData, contourNormalGeom, contourInstance, contourMaterial, contourLabel,
            # contourPriLdx, contourInvNormal
            3: "$DO.cb:$DO.cpd:$DO.cng:$DO.ci:$DO.cm:$DO.cl:$DO.cpi:$DO.cin",

            # CONTOURS: DRAW BY SAMPLE CONTRAST
            # enableContourColor, contourColor, enableContourDepth, contourDepth, enableContourDist, contourDist,
            # enableContourNormal, contourNormal, enableContourTexUV, contourTexU, contourTexV
            4: "$DO.ecc:$DO.cco:$DO.edp:$DO.cdp:$DO.ecd:$DO.cd:$DO.ecn:" \
                "$DO.cn:$DO.euv:$DO.ctu:$DO.ctv",

            # CONTOURS: CUSTOM SHADERS
            # contourContrast, contourStore
            5: "$DO.coc:$DO.cos",

            # ANTI-ALIASING QUALITY: RAYTRACE/SCANLINE QUALITY
            # minSamples, maxSamples, diagnoseSamples, contrastR, contrastG, contrastB, contrastA
            6: "$DO.minsp:$DO.maxsp:$DO.dias:$DO.conr:$DO.cong:$DO.conb:" \
                "$DO.cona",

            # ANTI-ALIASING QUALITY: RASTERIZER QUALITY
            # rapidSamplesCollect, rapidSamplesShading
            7: "$DO.rapc:$DO.raps",

            # ANTI-ALIASING QUALITY: MULTI-PIXEL FILTERING + SAMPLES OPTIONS
            # filter, filterWidth, filterHeight, jitter, sampleLock
            8: "$DO.fil:$DO.filw:$DO.filh:$DO.jit:$DO.splck",

            # RAYTRACING
            # rayTracing, maxReflectionRays, maxRefractionRays, maxRayDepth, maxShadowRayDepth, maxReflectionBlur,
            # maxRefractionBlur
            9: "$DO.ray:$DO.rflr:$DO.rfrr:$DO.maxr:$DO.shrd:$DO.rflb:$DO.rfrb",

            # RAYTRACING: ACCELERATION
            # accelerationMethod, bspSize, bspDepth, bspShadow, diagnoseBsp
            10: "$MG.acl:$MG.bsps:$MG.bspd:$MG.bspw:$DO.diab",

            # RASTERIZER

            # RASTERIZER: SHADOWS
            # shadowMethod, shadowsObeyShadowLinking, shadowsObeyLightLinking, shadowMaps, rebuildShadowMaps
            12: "$DO.shmth:$MG.sosl:$MG.soll:$DO.shmap:$DO.rsm",

            # MOTION BLUR
            # motionBlur, motionBlurBy, shutterDelay, shutter, motionBlurShadowMaps
            13: "$DO.mb:$DO.mbb:$DO.shud:$DO.shutter:$DO.mbsm",

            # MOTION BLUR: QUALITY
            # motionSteps, timeContrastR, timeContrastG, timeContrastB, timeContrastA, rapidSamplesMotion
            14: "$DO.mst:$DO.tconr:$DO.tcong:$DO.tconb:$DO.tcona:$DO.rapm",

            # MOTION BLUR: MOTION OFFSETS
            # exportCustomMotion, exportMotionOffset, exportMotionOutput
            15: "$MG.xcm:$MG.xmo:$MG.xmp",

            # FRAMEBUFFER
            # datatype, gamma, colorclip, interpolateSamples, desaturate, premultiply, dither
            16: "$DF.dat:$DF.gam:$DF.cclp:$DF.int:$DF.desat:$DF.prem:$DF.dith",

            # ENVIRONMENT
            # imageBasedLightning, sunAndSkyShader
            17: "$MG.ibl:$MG.sunAndSkyShader",

            # GLOBAL ILLUMINATIONS
            # globalIllumAccuracy, globalIllumScale, globalIllumRadius, globalIllumMerge
            18: "$DO.gia:$DO.gis:$DO.gir:$DO.gim",

            # CAUSTICS
            # causticAccuracy, causticScale, causticRadius, causticMerge, causticFilterType, causticFilterKernel
            19: "$DO.caa:$DO.cs:$DO.car:$DO.cam:$DO.caft:$DO.cafk",

            # PHOTON TRACING
            # maxReflectionPhotons, maxRefractionPhotons, maxPhotonDepth
            20: "$DO.rflp:$DO.rfrp:$DO.maxp",

            # PHOTON MAP
            # photonMapRebuild, photonMapFilename, photonMapVisualizer, shadowEffectsWithPhotons, diagnosePhoton,
            # diagnosePhotonDensity
            21: "$DO.pmr:$DO.pmf:$DO.pmv:$MG.shph:$DO.diap:$DO.dgpd",

            # PHOTON VOLUME
            # photonAutoVolume, photonVolumeAccuracy, photonVolumeRadius, photonVolumeMerge
            22: "$DO.phav:$DO.cava:$DO.cavr:$DO.phvm",

            # IMPORTONS

            # FINAL GATHERING
            # finalGatherRays, finalGatherPresampleDensity, finalGatherPoints, finalGatherScale, finalGatherBounceScale,
            # finalGatherTraceDiffuse
            24: "$DO.fgr:$DO.fgpd:$DO.fgpt:$DO.fgs:$DO.fgbs:$DO.fgtf",

            # FINAL GATHERING: FINAL GATHERING MAP
            # finalGatherRebuild, finalGatherFilename, finalGatherMergeFiles, finalGatherMapVisualizer, previewFinalGatherTiles,
            # diagnoseFinalg
            25: "$DO.fgrb:$DO.fgfn:$DO.fgmf:$DO.fgmz:$MG.pfgt:$DO.difg",

            # FINAL GATHERING: FINAL GATHERING QUALITY
            26: "$DO.fgfi:$DO.fgst:$DO.fgsp",

            # FINAL GATHERING: FINAL GATHERING TRACING
            27: "$DO.fgtl:$DO.fgtr:$DO.fgtd:$DO.fgmax:$DO.fgmin:$DO.fgvw",

            # IRRADIANCE PARTICLES

            # AMBIENT OCCLUSION

            # DIAGNOSTICS
            # diagnoseSamples, diagnoseBsp, diagnoseGrid, diagnoseGridSize, diagnosePhoton, diagnosePhotonDensity,
            # diagnoseFinalg
            30: "$DO.dias:$DO.diab:$DO.diag:$DO.dggs:$DO.diap:$DO.dgpd:" \
                "$DO.difg",

            # PREVIEW
            # previewAnimation, previewMotionBlur, previewRenderTiles, previewConvertTiles, previewTonemapTiles,
            # tonemapRangeHigh
            31: "$MG.pan:$MG.pmb:$MG.prt:$MG.pct:$MG.ptt:$MG.tmh",

            # MENTAL RAY OVERRIDES
            # maxDisplace, biasShadowMaps, approx, displaceApprox
            32: "$DO.madi:$DO.bism:$DO.apx:$DO.dapx",

            # TRANSLATION
            # exportExactHierarchy, exportFullDagpath, exportTexturesFirst, exportParticles, exportParticlesInstances,
            # exportFluids, exportHair, exportPostEffects, exportVertexColors
            33: "$MG.hier:$MG.fdag:$MG.xtf:$MG.xpt:$MG.xpti:$MG.xfl:$MG.xhr:" \
                "$MG.xpfx:$MG.xvc",

            # TRANSLATION: PERFORMANCE
            # exportAssignedOnly, exportVisibleOnly, optimizeAnimateDetection, exportSharedVertices, optimizeRaytraceShadows,
            # exportAssembly, exportMotionSegments, exportTriangles, exportShapeDeformation, forceMotionVectors,
            # exportPolygonDerivatives, mayaDerivatives, smoothPolygonDerivatives, exportNurbsDerivatives, exporObjectsOnDemand,
            # exportPlaceholderSize, allocateOnHeap
            34: "$MG.ass:$MG.inv:$MG.oad:$MG.xsv:$MG.ors:$MG.xasm:$MG.xmg:" \
                "$MG.xtr:$MG.xsd:$DO.fmv:$MG.xpd:$MG.myd:$MG.spd:$MG.xnd:" \
                "$MG.xod:$MG.xps:$DO.aoh",

            # TRANSLATION: CUSTOMIZATION
            # useLegacyShaders, exportStateShader, exportLightLinker, exportMayaOptions, exportCustomColors, exportCustom,
            # exportCustomData, exportCustomVectors
            35: "$MG.uls:$MG.xss:$MG.xll:$MG.xop:$MG.xcuc:$MG.xcu:$MG.xcud:" \
                "$MG.xcv",

            # CUSTOM ENTITIES
            # passAlphaThrough, passDepthThrough, passLabelThrough, versions, links, includes, miText, miTextOptions,
            # miTextLights, miTextCameras, miTextScene, miTextRoot, miTextRender
            36: "$MG.pat:$MG.pdt:$MG.plt:$MG.ver:$MG.lnk:$MG.inc:$MG.mitx:" \
                "$MG.mito:$MG.mitl:$MG.mitc:$MG.mits:$MG.mitt:$MG.mitr",
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

        return "%s -r mr -s %s -e %s -pad 4 -fnc 3 -v 5 -x %s -y %s " \
            "-cam %s -rd %s -im %s %s"

    def sections(self):
        """
        Returns all the sections of the render globals for the engine
        """

        return {
            0: "Rendering Features",
            1: "Extra Features",
            2: "Contours",
            3: "Contours: Draw By Property Difference",
            4: "Contours: Draw By Sample Contrast",
            5: "Contours: Custom Shaders",
            6: "Anti-Aliasing Quality: Raytrace/Scanline Quality",
            7: "Anti-Aliasing Quality: Rasterizer Quality",
            8: "Anti-Aliasing Quality: Multi-Pixel Filtering + Sample Options",
            9: "Raytracing",
            10: "Acceleration",
            11: "Rasterizer",
            12: "Shadows",
            13: "Motion Blur",
            14: "Motion Blur: Quality",
            15: "Motion Blur: Motion Offsets",
            16: "Framebuffer",
            17: "Environment",
            18: "Global Illumination",
            19: "Caustics",
            20: "Photon Tracing",
            21: "Photon Map",
            22: "Photon Volume",
            23: "Importons",
            24: "Final Gathering",
            25: "Final Gathering: Final Gathering Map",
            26: "Final Gathering: Final Gathering Quality",
            27: "Final Gathering: Final Gathering Tracing",
            28: "Irradiance Particles",
            29: "Ambient Occlusion",
            30: "Diagnostics",
            31: "Preview",
            32: "mental ray Overrides",
            33: "Translation",
            34: "Performance",
            35: "Customization",
            36: "Custom Entities",
        }

    def setup(self):
        """
        Makes sure the engine is loaded and that the render globals nodes 
        exists. This is executed on each startup of Sandwich but does only 
        takes time if the engine is loaded for the first time.
        """

        self.bIsInstalled = False

        # Check if mental ray plugin is loaded. If not, load it
        if not mc.pluginInfo("Mayatomr", query = True, loaded = True):
            mc.loadPlugin("Mayatomr")

        # Check if render globals nodes exists. If not, create them
        if not mc.objExists("mentalrayGlobals"):
            mel.eval("miCreateDefaultNodes();")

        self.bIsInstalled = True