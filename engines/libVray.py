#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Engine "VRay"

This adds support for VRay

"""

import maya.cmds as mc
import maya.mel as mel


class Engine(object):
    def __init__(self, iMayaVersion):
        self.iMayaVersion = iMayaVersion
        self.sEngineName = "vray"
        self.sDisplayName = "V-Ray"
        self.lstNodes = (("vraySettings", "$VS"), 
            ("vrayEnvironmentPreview", "$VEP"))
        self.bIsInstalled = False

    def attributes(self):
        """

        """

        return {
            # GLOBAL OPTIONS: GEOMETRY
            0: "$VS.gogd:$VS.gogdh:$VS.gobc:$VS.gorvs:$VS.gumsfp",

            # GLOBAL OPTIONS: LIGHTNING
            1: "$VS.goldl:$VS.golddl:$VS.goldhl:$VS.golds:$VS.gologi",

            # GLOBAL OPTIONS: GI
            2: "$VS.gogdri",

            # GLOBAL OPTIONS: MATERIALS
            3: "$VS.gomrr:$VS.gomld:$VS.gommd:$VS.gomdm:$VS.gomfm:$VS.gomtml:$VS.gomtc:$VS.gomg",

            # GLOBAL OPTIONS: RAYTRACING
            4: "$VS.gomb",

            # IMAGE SAMPLER: ANTIALIASING FILTER
            5: "$VS.st:$VS.aafon:$VS.aaft:$VS.aafs",

            # IMAGE SAMPLER: FIXED RATE
            6: "$VS.fsd",

            # IMAGE SAMPLER: ADAPTIVE DMC
            7: "$VS.dmi:$VS.dma:$VS.dmlt:$VS.dmt:$VS.dss",

            # IMAGE SAMPLER: ADAPTIVE SUBDIVISION
            8: "$VS.smi:$VS.sma:$VS.sji:$VS.tre:$VS.sde:$VS.sno:$VS.snot:$VS.sss",

            # ENVIRONMENT
            9: "$VS.caoet:$VS.caet1:$VS.caet2:$VS.caet3:$VS.caet4:$VEP.vpte:$VEP.ttu:$VEP.vpr:$VEP.vpss:$VEP.vptsrgb:" \
               "$VEP.vpg:$VS.caevo:$VS.caev",

            # COLOR MAPPING
            10: "$VS.cmtp:$VS.cmdm:$VS.cmbm:$VS.cg:$VS.cmab:$VS.cmsm:$VS.cmao:$VS.cmlw:$VS.cmco:$VS.cmcl:$VS.cmas",

            # CAMERA: CAMERA TYPE
            11: "$VS.catype:$VS.caofov:$VS.cahei:$VS.caaf:$VS.cadi:$VS.cacu",

            # CAMERA: DEPTH OF FIELD
            12: "$VS.cadon:$VS.cadap:$VS.cacebi:$VS.cadgfc:$VS.cadfd:$VS.cads:$VS.cadsn:$VS.cadrt:$VS.cadani:$VS.cadsubd",

            # CAMERA: MOTION BLUR
            13: "$VS.camon:$VS.cammb:$VS.camdur:$VS.camic:$VS.cabias:$VS.casef:$VS.camsd:$VS.capps:$VS.camgs",

            # MISC
            14: "$VS.bmpm:$VS.tfsm:$VS.phsc:$VS.neg",

            # VRAY UI
            15: "$VS.uirs:$VS.uisbt:$VS.uidefbg",

            # GI
            16: "$VS.gi:$VS.rfc:$VS.rrc",

            # GI: POST-PROCESSING
            17: "$VS.sat:$VS.cnt:$VS.ctb",

            # GI: AMBIENT OCCLUSION
            18: "$VS.ao:$VS.aoa:$VS.aor:$VS.aos",

            # GI: PRIMARY BOUNCES
            19: "$VS.pe:$VS.pm",

            # GI: SECONDARY BOUNCES
            20: "$VS.se:$VS.sm",

            # GI: RAY DISTANCE
            21: "$VS.rdiston:$VS.rdist",

            # PHOTON MAP
            22: "$VS.pmbs:$VS.pmmph:$VS.pmpf:$VS.pmpfs:$VS.pmche:$VS.pmrtb:$VS.pmsdl:$VS.pmasd:$VS.pmmlt:$VS.pmrtc:" \
                "$VS.pmmxd",

            # PHOTON MAP: MODE
            23: "$VS.pmmd:$VS.pmfile",

            # PHOTON MAP: ON RENDER END
            24: "$VS.pmdd:$VS.pmasv:$VS.pmasf",

            # CAUSTICS
            25: "$VS.con:$VS.cmul:$VS.csd:$VS.cmph:$VS.cmd",

            # CAUSTICS: MODE
            26: "$VS.cmod:$VS.cfile",

            # CAUSTICS: ON RENDER END
            27: "$VS.cdnd:§VS.casv:$VS.casf",

            # DMC SAMPLER
            28: "$VS.dmcstd:$VS.dmcsaa:$VS.dmcsat:$VS.dmcsams:$VS.dmcssm",
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

    def sections(self):
        """
        Returns all the sections of the render globals for the engine
        """

        return {
            0: "Global Options: Geometry",
            1: "Global Options: Lightning",
            2: "Global Options: GI",
            3: "Global Options: Materials",
            4: "Global Options: Raytracing",
            5: "Image Sampler: Antialiasing Filter",
            6: "Image Sampler: Fixed Rate",
            7: "Image Sampler: Adaptive DMC",
            8: "Image Sampler: Adaptive Subdivision",
            9: "Environment",
            10: "Color Mapping",
            11: "Camera: Camera Type",
            12: "Camera: Depth of Field",
            13: "Camera: Motion Blur",
            14: "Misc",
            15: "V-Ray Sun and Sky",
            16: "Vray UI",
            17: "GI",
            18: "GI: Post-Processing",
            19: "GI: Ambient Occlusion",
            20: "GI: Primary Bounces",
            21: "GI: Secondary Bounces",
            22: "GI: Ray Distance",
            23: "GI: Engine Specific Options",
            24: "Caustics",
            25: "Caustics: Mode",
            26: "Caustics: On Render End",
            27: "DMC Sampler",
            28: "Default Displacement and Subdivision",
            29: "System: Raycaster Params",
            30: "System: Render Region Division",
            31: "System: Distributed Rendering",
            32: "System: VRay Log",
            33: "System: Frame Stamp",
            34: "System: Other",
            35: "Translator",
            36: "Render Elements",
            37: "Shading",
            38: "Performance",
            39: "Rendering",
            40: "Adaptive Sampling",
            41: "Locks",
            42: "Engine",
            43: "Stereo Vision",
            44: "Geometry",
        }

    def setup(self):
        """
        Makes sure the engine is loaded and that the render globals nodes 
        exists. This is executed on each startup of Sandwich but does only 
        takes time if the engine is loaded for the first time.
        """

        self.bIsInstalled = False

        # TODO: Ugly solution! How do we check if a plugin exists or not?
        try:
            # Check if vray plugin is loaded. If not, load it
            if not mc.pluginInfo("vrayformaya", query = True, loaded = True):
                mc.loadPlugin("vrayformaya")

            # Check if render globals nodes exists. If not, create them
            if not mc.objExists("vraySettings"):
                mel.eval("vrayCreateVRaySettingsNode();")

            self.bIsInstalled = True

        except:
            pass